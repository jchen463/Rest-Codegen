import sys
import os
import importlib.util
import yaml
import ast
import json
import argparse

from openapi_spec_validator import openapi_v3_spec_validator

try:  # when just doing $ python3 main.py only below imports work
    import codegen.codegen_config as cfg
    from codegen.classes import Specification
except ImportError as err:  # when packaged, only above imports work
    import codegen_config as cfg
    from classes import Specification


def main():
    if len(sys.argv) > 1:
        cfg.load_build_file(sys.argv[1])

    if cfg.LANGUAGE == 'flask':
        try:
            from codegen.flask_server_codegen import flask_server_codegen as codegen
            from codegen.flask_server_codegen import stage_default_iterators
        except ImportError as err:
            from flask_server_codegen import flask_server_codegen as codegen
            from flask_server_codegen import stage_default_iterators
    if cfg.LANGUAGE == 'typescript':
        try:
            from codegen.typescript_client_codegen import typescript_client_codegen as codegen
            from codegen.typescript_client_codegen import stage_default_iterators
        except ImportError as err:
            from typescript_client_codegen import typescript_client_codegen as codegen
            from typescript_client_codegen import stage_default_iterators

    stage_default_iterators()

    if len(sys.argv) > 1:
        cfg.load_build_file(sys.argv[1])

    print(sys.argv)
    print(cfg.SPEC)
    print(cfg.SPEC_FILE_PATH)

    cfg.SPEC_DICT = load_spec_file(cfg.SPEC_FILE_PATH)
    validate_specification(cfg.SPEC_DICT)
    cfg.SPECIFICATION = Specification(cfg.SPEC_DICT)
    spec_dict2 = ast.literal_eval(str(vars(cfg.SPECIFICATION)))

    # print(cfg.SPECIFICATION.paths.dikt['/pet'].post)
    # print(type(cfg.SPECIFICATION.paths.dikt['/pet'].post))

    # with open('spec_tree.json', 'wt') as out:
    #     json.dump(spec_dict2, out, indent=4)

    codegen()


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
