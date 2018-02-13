import json
import os.path
import sys

import yaml
from openapi_spec_validator import openapi_v3_spec_validator

import app_config as cfg
from classes.parse import parse_dict


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


def process_tree(spec):
    """
    Modify tree here. Parse through and fill out the components section accordingly?
    How to resolve of dependencies between components???
    Ex. An attribute of Pet is a Category
        What if we're constructing a Schema instance for Pet.
        We want to first have the Schema instance for category made, etc.
    How to parse through the dictionary tree such that we can link all references
    """
    pass


def generate_flask_server_code(spec):
    pass


def main():
    spec = load_spec_file(cfg.SPEC_FILES[0])
    validate_specification(spec)
    print(type(spec['servers']))
    spec2 = parse_dict(spec,
                       allowed=['openapi', 'info', 'server', 'paths',
                                'components', 'security', 'tags', 'externalDocs'],
                       required=['openapi', 'info', 'paths'],
                       objects=['info', 'paths', 'components', 'externalDocs'],
                       arrays=['server', 'security', 'tags'])


if __name__ == '__main__':
    main()
