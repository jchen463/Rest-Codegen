import sys
import os
import importlib.util
import yaml
import ast
import json

from openapi_spec_validator import openapi_v3_spec_validator

from codegen.classes.specification import Specification
from codegen.flask_server_codegen import flask_server_codegen


SPEC = 'swagger.yaml'
SPEC_FILE_PATH = os.getcwd() + '/' + DEFAULT_SPEC

PROJECT_OUTPUT = os.getcwd()


def main(build_file=None):
    if build_file is not None:
        load_build_file(build_file)

    spec_dict = load_spec_file(SPEC)
    spec = Specification(spec_dict)
    spec_tree_dict = ast.literal_eval(str(vars(spec)))

    with open('spec_tree.json', 'wt') as out:
        json.dump(spec_tree_dict, out, indent=4)

    flask_server_codegen(spec_dict, build_file)


def load_build_file(filename):
    cwd = os.getcwd()
    full_path = cwd + '/' + filename
    spec = importlib.util.spec_from_file_location(
        filename[:-3], full_path)
    build_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build_script)


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


if __name__ == '__main__':
    if len(argv) > 1:
        main(sys.argv[1])
    else:
        main()
