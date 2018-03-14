import sys
import os
import importlib.util


BUILD = None
BUILD_FILE_PATH = None

SPEC = 'swagger.yaml'
SPEC_FILE_PATH = os.getcwd() + os.path.sep + SPEC

SPEC_DICT = None
SPECIFICATION = None

# PROJECT_NAME = 'generated'
# PROJECT_OUTPUT = os.getcwd() + os.path.sep + PROJECT_NAME
# SERVER_NAME = PROJECT_NAME
# SERVER_OUTPUT = PROJECT_OUTPUT + os.path.sep + PROJECT_NAME

LANGUAGE = 'flask'

FLASK_PROJECT_NAME = 'flask-server-generated'
FLASK_PROJECT_OUTPUT = os.getcwd() + os.path.sep + FLASK_PROJECT_NAME
FLASK_SERVER_NAME = 'flask_server'
FLASK_SERVER_OUTPUT = FLASK_PROJECT_OUTPUT + os.path.sep + FLASK_SERVER_NAME

TYPESCRIPT_PROJECT_NAME = 'services'
TYPESCRIPT_PROJECT_OUTPUT = os.getcwd() + os.path.sep + TYPESCRIPT_PROJECT_NAME


# not implemented yet
# USER_TEMPLATES_NAME = None
# USER_TEMPLATES_PATH = None

# DEFAULT_TEMPLATES_DIR = 'templates'


def load_build_file(filename):
    # update defaults to reflect user's build file
    global BUILD
    global BUILD_FILE_PATH
    global SPEC
    global SPEC_FILE_PATH
    global SPEC_DICT
    global SPECIFICATION
    global LANGUAGE
    global FLASK_PROJECT_NAME
    global FLASK_PROJECT_OUTPUT
    global FLASK_SERVER_NAME
    global FLASK_SERVER_OUTPUT
    global TYPESCRIPT_PROJECT_NAME
    global TYPESCRIPT_PROJECT_OUTPUT

    print('loading build file:', filename)
    filepath = os.getcwd() + '/' + filename
    spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
    build_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build_script)

    BUILD = filename
    BUILD_FILE_PATH = filepath

    if hasattr(build_script, 'SPEC'):
        SPEC = build_script.SPEC
        SPEC_FILE_PATH = os.getcwd() + os.path.sep + SPEC
    if hasattr(build_script, 'LANGUAGE'):
        LANGUAGE = build_script.LANGUAGE
