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

FLASK_PROJECT_NAME = 'flask-server-generated'
FLASK_PROJECT_OUTPUT = os.getcwd() + os.path.sep + FLASK_PROJECT_NAME
FLASK_SERVER_NAME = 'flask-server'
FLASK_SERVER_OUTPUT = FLASK_PROJECT_OUTPUT + os.path.sep + FLASK_SERVER_NAME

TYPESCRIPT_PROJECT_NAME = 'typescript-client-generated'
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
    global PROJECT_NAME
    global PROJECT_OUTPUT
    global SERVER_NAME
    global SERVER_OUTPUT

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
    if hasattr(build_script, 'PROJECT_NAME'):
        PROJECT_NAME = build_script.PROJECT_NAME
        PROJECT_OUTPUT = os.getcwd() + os.path.sep + PROJECT_NAME
        SERVER_NAME = PROJECT_NAME
        SERVER_OUTPUT = PROJECT_OUTPUT + os.path.sep + PROJECT_NAME
    if hasattr(build_script, 'SERVER_NAME'):
        SERVER_NAME = build_script.SERVER_NAME
        SERVER_OUTPUT = PROJECT_OUTPUT
