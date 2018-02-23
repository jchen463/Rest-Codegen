from collections import namedtuple
import os.path

import jinja2

from classes.parse import get_object


def output_model_class(spec):
    makeFirstLetterLower = lambda s: s[:1].lower() + s[1:] if s else ''

    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    file_name = "base_model_.py"
    renders = [FileRender('templates/base_model.tmpl', file_name, [])]
    do_renders(renders, 'templates/', 'models')

    # print(spec['components'].schemas)
    for scheme_name, schema_obj in spec.components.schemas.items():

        model = {
            'name': makeFirstLetterLower(scheme_name),
            'properties': [],
        }

        model_lib = {
            'libraries': [
                {'name': 'json'},
            ]
        }
        model_dep = {
            'dependencies': [
               # {'location': 'base_model_', 'object': 'Model'}
            ]
        }

        for prop_name, attribute in schema_obj.properties.items():

            attribute_type = ""

            if 'ref' in attribute.__dict__:
                attribute_type += attribute.ref[attribute.ref.rfind('/') + 1:]
                model_dep['dependencies'].append({'location': makeFirstLetterLower(attribute_type), 'object': attribute_type})
            elif attribute.type == 'string':
                attribute_type += 'str'
            elif attribute.type == 'integer':
                attribute_type += 'int'
            elif attribute.type == 'number':
                attribute_type += 'float'
            elif attribute.type == 'array':
                # print(attribute)
                #print(attribute.items)
                temp = attribute.items
                attribute_type += 'List['
                array_num = 1

                #untested while loop
                while hasattr(temp, 'type'):
                    if temp.type == 'array':
                        temp = attribute.items
                        array_num += 1
                    else:
                        break

                if 'ref' in attribute.items.__dict__:
                    attribute_type += attribute.items.ref[attribute.items.ref.rfind('/') + 1:]
                    model_dep['dependencies'].append({'location': makeFirstLetterLower(attribute.items.ref[attribute.items.ref.rfind('/') + 1:]), 'object': attribute.items.ref[attribute.items.ref.rfind('/') + 1:]})
                elif attribute.items.type == 'string':
                    attribute_type += 'str'
                elif attribute.items.type == 'integer':
                    attribute_type += 'int'
                elif attribute.items.type == 'number':
                    attribute_type += 'float'

                for _ in range(array_num):
                    attribute_type += ']'

                #untested while loop:
                #while attribute.items.type
                #attribute_type = '[]' # this will need to be fixed

            if attribute_type != "":
                model['properties'].append(
                    {
                        'name': prop_name,
                        'type': attribute_type
                    }
                )

        file_name = model['name'] + ".py"
        renders = [FileRender('templates/models.tmpl', file_name, [
            model_lib, model_dep, model])]
        do_renders(renders, 'templates/', 'models')


def generate_flask_server_code(spec):
    output_model_class(spec)


def do_renders(renders, template_dir, output_dir):

    # Create the Jinja2 environment using custom options and loader, see sections below.
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        ''), trim_blocks=True, lstrip_blocks=True, line_comment_prefix='//*')

    for render in renders:

        # Merge the dictionnaries
        params = {}
        for param_dict in render.params_dicts:
            params.update(param_dict)

        # Render the template
        output = env.get_template(render.template).render(**params)

        # Output the file, creating directories if needed.
        output_file = output_dir + os.path.sep + render.output
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(output_file, 'w') as outfile:
            outfile.write(output)
