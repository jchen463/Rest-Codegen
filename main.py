import json
import os.path
import sys

import yaml
from openapi_spec_validator import openapi_v3_spec_validator

import app_config as cfg


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


def main():
    spec = load_spec_file(cfg.SPEC_FILES[0])
    validate_specification(spec)


class Wrapper:
    def __init__(self, data):
        self.data = data


if __name__ == '__main__':
    main()
