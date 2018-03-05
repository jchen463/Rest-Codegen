from collections import namedtuple
import os.path

import jinja2

from codegen.classes import get_object

FileRender = namedtuple('FileRender', ['template', 'output', 'params_dicts'])

methods = {
        'methods': ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']
    }

def generate_flask_server_code(spec, spec_dict):
    output_main()
    output_encoder()
    output_util()
    output_controllers(spec_dict)
    output_requirements()
    output_init()
    output_model_class(spec)


def generate_typescript_client_code(spec, spec_dict):
    output_client_api(spec_dict);
    output_client_model(spec_dict);

def output_client_model(spec_dict):

    type_map = {'integer': 'number', 'string': 'string', 'array': None, 'boolean': 'boolean' }

    for key, value in spec_dict['components']['schemas'].items():

        models = {'model_name': key,
                'properties': [],
                'required': value['required']}

        for attribute, attribute_type in value['properties'].items():
            name = attribute
            if 'type' in attribute_type:
                if attribute_type['type'] != 'array':
                    val_type = attribute_type['type']
                    var_type = type_map[val_type]
                else:
                    if 'type' in attribute_type['items']:
                        item = attribute_type['items']['type']
                        var_type = 'Array<' + type_map[item] +'>'
                    elif '$ref' in attribute_type['items']:
                        item = attribute_type['items']['$ref']
                        var_type = 'Array<' + item +'>'
                    else: 
                        var_type = 'Array<' + 'None' + '>'
            else:
                var_type = 'none'
            
            if '$ref' in attribute_type:
                ref = attribute_type['$ref']
            else:
                ref = 'none'
            
            if 'enum' in attribute_type:
                enum = attribute_type['enum']

            new_attribute = { 'name': name, 'type': var_type, 'ref': ref, 'enum': enum }
            models['properties'].append(new_attribute)

        file_name = key + '.ts'
        model_name = {'model_name': key}
        renders = [FileRender('templates/client_models.tmpl', file_name, [models])]
        do_renders(renders, 'templates/', 'generated/client/models')

def output_client_api(spec_dict):
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

    for tag in tags['tags']:
        file_name = tag.capitalize() + 'Api.ts'
        tag = {'tag': tag}
        renders = [FileRender('templates/client_api.tmpl', file_name,
                              [controller_dep, tags, controller_functions, methods, basePath])]
        do_renders(renders, 'templates/', 'generated/client/api')

def output_init():
    file_name = '__init__.py'
    renders = [FileRender('codegen/templates/init.tmpl', file_name, [])]
    do_renders(renders, 'codegen/templates/', 'codegen/generated')


def output_requirements():
    file_name = 'requirements.txt'
    renders = [FileRender(
        'codegen/templates/requirements.tmpl', file_name, [])]
    do_renders(renders, 'codegen/templates/', 'codegen/generated')


def output_main():

    file_name = '__main__.py'
    renders = [FileRender('codegen/templates/main.tmpl', file_name, [])]
    do_renders(renders, 'codegen/templates/', 'codegen/generated')


def output_encoder():

    file_name = 'encoder.py'
    renders = [FileRender('codegen/templates/encoder.tmpl', file_name, [])]
    do_renders(renders, 'codegen/templates/', 'codegen/generated')


def output_util():

    file_name = 'util.py'
    renders = [FileRender('codegen/templates/util.tmpl', file_name, [])]
    do_renders(renders, 'codegen/templates/', 'codegen/generated')


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
    renders = [FileRender('codegen/templates/controller.tmpl', file_name,
                          [controller_lib, controller_dep, controller_functions, methods])]
    do_renders(renders, 'codegen/templates/', 'codegen/generated/controllers')


def output_model_class(spec):
    def makeFirstLetterLower(s):
        return s[:1].lower() + s[1:] if s else ''

    file_name = "base_model_.py"
    renders = [FileRender('codegen/templates/base_model.tmpl', file_name, [])]
    do_renders(renders, 'codegen/templates/', 'codegen/generated/models')

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
        do_renders(renders, 'codegen/templates/', 'codegen/generated/models')


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
