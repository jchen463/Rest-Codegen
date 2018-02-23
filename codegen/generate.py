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
        # print(value)
        key = key.replace('{', '<')
        key = key.replace('}', '>')
        # for char in key:
        #     if char == '{':
        #         new_key += '<'
        #         param_type = ''
        #         # for method in methods['methods']:
        #         #     if value[method] is not None and value[method]['parameters'] != [] and value[method]['parameters']['schema'] is not None and value[method]['parameters']['schema']['type'] is not None:
        #         #         param_type = value[method]['parameters']['schema']['type']
        #         #         print(param_type)
        #         #         break
        #         new_key += type_mapping[param_type]
        #         if key[len(new_key) - 1] != '{':
        #             new_key += ':'
        #     elif char == '}':
        #         new_key += '>'
        #     else:
        #         new_key += char
        # print(new_key)
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
    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])
    models = []
    for scheme_name, schema_obj in spec.components.schemas.items():
        model_class = {
            'classes': [
                {
                    'name': scheme_name,
                    'arguments': [],
                    'init_args': [],
                    'class_methods': []
                }
            ]
        }

        for prop_name, attributes in schema_obj.properties.items():
            if 'ref' in attributes.__dict__:
                print('ye')
            else:
                model_class['classes'][0]['init_args'].append(
                    {
                        'name': prop_name,
                        'type': attributes.type
                    }
                )

        models.append(model_class)

    model_lib = {
        'libraries': [
            {'name': 'json'},
        ]
    }

    model_dep = {
        'dependencies': [
            {'location': 'flask', 'object': 'Blueprint'},
            {'location': 'flask', 'object': 'jsonify'},
        ]
    }

    for model_class in models:
        file_name = model_class['classes'][0]['name'] + ".py"
        renders = [FileRender('templates/models.tmpl', file_name, [
            model_lib, model_dep, model_class])]
        do_renders(renders, 'templates/', 'models')


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
