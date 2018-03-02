from collections import namedtuple
import os.path

import jinja2

from classes.parse import get_object


def generate_flask_server_code(spec, spec_dict):
    output_main()
    output_encoder()
    output_util()
    output_controllers(spec_dict)
    output_requirements()
    output_init()
    output_model_class(spec)

def generate_typescript_client_code(spec, spec_dict):
    output_client_api(spec_dict, spec);

def output_client_api(spec_dict, spec):

    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    methods = {
        'methods': ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']
    }

    tags = {'tags': [] }

    for tag in spec_dict['tags']:
        tags['tags'].append(tag['name'])

    basePath = {'url': spec_dict['servers'][0]['url'] }

    controller_functions = {'dikt': {}}
    for key, value in spec_dict['paths']['dikt'].items():
        key = key.replace('{', '<')
        key = key.replace('}', '>')
        controller_functions['dikt'][key] = value

    controller_dep = {
        'dependencies': [
            {'location': '@angular/core', 'objects': ['Inject', 'Injectable', 'Optional'] },
            {'location': '@angular/http', 'objects': ['Http', 'Headers', 'URLSearchParams'] },
            {'location': '@angular/http', 'objects': ['RequestMethod', 'RequestOptions', 'RequestOptionsArgs'] },
            {'location': '@angular/http', 'objects': ['Response, ResponseContentType']},
            {'location': 'rxjs/Observable', 'objects': ['Observable']},
            {'location': '../variables', 'objects': ['BASE_PATH', 'COLLECTION_FORMATS']},
            {'location': '../configuration', 'objects': ['Configuration']}
        ]
    }

    file_name = 'default_client_api.py'
    renders = [FileRender('templates/client_api.tmpl', file_name,
                          [controller_dep, tags, controller_functions, methods, basePath])]
    do_renders(renders, 'templates/', 'generated/client/api')
    
def output_init():
    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    file_name = '__init__.py'
    renders = [FileRender('templates/init.tmpl', file_name, [])]
    do_renders(renders, 'templates/', 'generated')


def output_requirements():
    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    file_name = 'requirements.txt'
    renders = [FileRender('templates/requirements.tmpl', file_name, [])]
    do_renders(renders, 'templates/', 'generated')


def output_main():
    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    file_name = '__main__.py'
    renders = [FileRender('templates/main.tmpl', file_name, [])]
    do_renders(renders, 'templates/', 'generated')


def output_encoder():
    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    file_name = 'encoder.py'
    renders = [FileRender('templates/encoder.tmpl', file_name, [])]
    do_renders(renders, 'templates/', 'generated')


def output_util():
    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    file_name = 'util.py'
    renders = [FileRender('templates/util.tmpl', file_name, [])]
    do_renders(renders, 'templates/', 'generated')


type_mapping = {
    'integer': 'int',
    'long': 'int',
    'float': 'float',
    'double': 'float',
    'string': 'str',
    'byte': 'str',
    'binary': 'str',
    'boolean': 'bool',
    'date': 'str',
    'dateTime': 'str',
    'password': 'str',
    '': ''
}


def output_controllers(spec_dict):
    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    methods = {
        'methods': ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']
    }

    controller_functions = {'dikt': {}}
    for key, value in spec_dict['paths']['dikt'].items():
        key = key.replace('{', '<')
        key = key.replace('}', '>')
        controller_functions['dikt'][key] = value

    controller_lib = {
        'libraries': [
            {'name': 'json'},
        ]
    }

    controller_dep = {
        'dependencies': [
            {'location': 'flask', 'object': 'Blueprint'},
            {'location': 'flask', 'object': 'jsonify'},
            {'location': 'flask', 'object': 'abort'},
            {'location': 'flask', 'object': 'make_response'},
            {'location': 'flask', 'object': 'request'},
        ]
    }

    file_name = 'default_controller.py'
    renders = [FileRender('templates/controller.tmpl', file_name,
                          [controller_lib, controller_dep, controller_functions, methods])]
    do_renders(renders, 'templates/', 'generated/controllers')


def output_model_class(spec):
    def makeFirstLetterLower(s):
        return s[:1].lower() + s[1:] if s else ''

    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])

    file_name = "base_model_.py"
    renders = [FileRender('templates/base_model.tmpl', file_name, [])]
    do_renders(renders, 'templates/', 'generated/models')

    # print(spec['components'].schemas)
    for scheme_name, schema_obj in spec.components.schemas.items():

        model = {
            'name': scheme_name,
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
                model_dep['dependencies'].append(
                    {'location': makeFirstLetterLower(attribute_type), 'object': attribute_type})
            elif attribute.type == 'string':
                attribute_type += 'str'
            elif attribute.type == 'integer':
                attribute_type += 'int'
            elif attribute.type == 'number':
                attribute_type += 'float'
            elif attribute.type == 'array':
                # print(attribute)
                # print(attribute.items)
                temp = attribute.items
                attribute_type += 'List['
                array_num = 1

                # untested while loop
                while hasattr(temp, 'type'):
                    if temp.type == 'array':
                        temp = attribute.items
                        array_num += 1
                    else:
                        break

                if 'ref' in attribute.items.__dict__:
                    attribute_type += attribute.items.ref[attribute.items.ref.rfind(
                        '/') + 1:]
                    model_dep['dependencies'].append({'location': makeFirstLetterLower(attribute.items.ref[attribute.items.ref.rfind(
                        '/') + 1:]), 'object': attribute.items.ref[attribute.items.ref.rfind('/') + 1:]})
                elif attribute.items.type == 'string':
                    attribute_type += 'str'
                elif attribute.items.type == 'integer':
                    attribute_type += 'int'
                elif attribute.items.type == 'number':
                    attribute_type += 'float'

                for _ in range(array_num):
                    attribute_type += ']'

                # untested while loop:
                # while attribute.items.type
                # attribute_type = '[]' # this will need to be fixed

            if attribute_type != "":
                model['properties'].append(
                    {
                        'name': prop_name,
                        'type': attribute_type
                    }
                )

        file_name = makeFirstLetterLower(model['name']) + ".py"
        renders = [FileRender('templates/models.tmpl', file_name, [
            model_lib, model_dep, model])]
        do_renders(renders, 'templates/', 'generated/models')


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
        output = env.get_template(render.template).render(params)

        # Output the file, creating directories if needed.
        output_file = output_dir + os.path.sep + render.output
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(output_file, 'w') as outfile:
            outfile.write(output)
