import sys
import os
import importlib.util


def main(config_file_name):
    cwd = os.getcwd()
    full_path = cwd + '/' + config_file_name
    print(full_path)
    spec = importlib.util.spec_from_file_location(
        config_file_name[:-3], full_path)
    user_config_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_config_script)


if __name__ == '__main__':
    main(sys.argv[1])
