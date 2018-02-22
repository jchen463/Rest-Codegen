import json
import os.path
import sys
import yaml
from collections import namedtuple
import pprint
import ast

import jinja2
from openapi_spec_validator import openapi_v3_spec_validator

import app_config as cfg
# from classes.parse import parse_dict
from classes.parse import get_object
from classes.specification import Specification


FileRender = namedtuple('FileRender', ['template', 'output', 'params_dicts'])


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


def load_spec_file(file_path):
    extension = os.path.splitext(file_path)[1][1:]
    if extension == 'yaml' or 'yml':
        with open(file_path) as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(e)
                sys.exit()
    if extension == 'json':
        with open(file_path) as f:
            try:
                return json.load(f)
            except ValueError as e:
                print(e)
                sys.exit()


def validate_specification(spec):
    errors_iterator = openapi_v3_spec_validator.iter_errors(spec)
    l = list(errors_iterator)
    if (len(l) > 0):
        print(len(l), 'errors')
        sys.exit()

    print('specification is valid')


def output_model_class(spec):
    FileRender = namedtuple(
        'FileRender', ['template', 'output', 'params_dicts'])
    models = []
    # print(spec['components'].schemas)
    for scheme_name, schema_obj in spec['components'].schemas.items():
        print(scheme_name)
        print(schema_obj)
        print(schema_obj.__dict__)
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
            print(prop_name)
            print(attributes)
            print(attributes.__dict__)
            if 'ref' in attributes.__dict__:
                print('ye')
                print(get_object('schemas', attributes.__dict__))
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
            {'location': 'flask', 'object': 'jsonify'}
        ]
    }

    for model_class in models:
        file_name = model_class['classes'][0]['name'] + ".py"
        renders = [FileRender('templates/models.tmpl', file_name, [
            model_lib, model_dep, model_class])]
        do_renders(renders, 'templates/', 'models')


def generate_flask_server_code(spec):
    # output_model_class(spec)
    pass


def main():
    spec_dict = load_spec_file(cfg.SPEC_FILES[0])
    validate_specification(spec_dict)

    spec = Specification(spec_dict)
    spec_dict2 = ast.literal_eval(str(vars(spec)))

    # two options to print this. helpful for debugging
    # pprint.pprint(spec_dict2['info'])
    print(json.dumps(spec_dict2['info'], indent=4))

    # with open('sample/spec_tree.json', 'wt') as out:
    #     json.dump(spec_dict2, out, indent=4)

    # PROBABLY NOT THIS ONE
    # with open('sample/spec_tree.txt', 'wt') as out:    
    #     pprint.pprint(spec_dict2, stream=out)







if __name__ == '__main__':
    main()
