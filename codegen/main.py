import sys
import os
import importlib.util
import yaml
import ast
import json

from openapi_spec_validator import openapi_v3_spec_validator

from codegen.classes.specification import Specification
from codegen.flask_server_codegen import flask_server_codegen


SPEC = 'default.yaml'
SPEC_FILE_PATH = os.getcwd() + '/' + SPEC

BUILD = None
BUILD_FILE_PATH = None
if len(sys.argv) > 1:
    BUILD = sys.argv[1]
    BUILD_FILE_PATH = os.getcwd() + '/' + BUILD

PROJECT_OUTPUT = os.getcwd()


def main():
    if BUILD is not None:
        print('loading build file:', BUILD)
        spec = importlib.util.spec_from_file_location(
            BUILD[:-3], BUILD_FILE_PATH)
        build_script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_script)
        SPEC = build_script.SPEC

    spec_dict = load_spec_file(SPEC)
    spec = Specification(spec_dict)
    spec_tree_dict = ast.literal_eval(str(vars(spec)))

    # with open('spec_tree.json', 'wt') as out:
    #     json.dump(spec_tree_dict, out, indent=4)

    flask_server_codegen(spec_dict, BUILD)


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
    main()
