import json
import os.path
import sys
import yaml
import pprint
import ast

from openapi_spec_validator import openapi_v3_spec_validator

import app_config as cfg
from classes.specification import Specification
from generate import generate_flask_server_code


def main():
    spec_dict = load_spec_file(cfg.SPEC_FILES[0])
    validate_specification(spec_dict)

    spec = Specification(spec_dict)
    spec_dict2 = ast.literal_eval(str(vars(spec)))

    # pprint.pprint(spec_dict2['info'])
    # print(json.dumps(spec_dict2['paths'], indent=4))
    with open('spec_tree.json', 'wt') as out:
        json.dump(spec_dict2, out, indent=4)

    generate_flask_server_code(spec)


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
