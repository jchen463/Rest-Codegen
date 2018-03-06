import sys
import os


BUILD = None
BUILD_FILE_PATH = None

SPEC = 'swagger.yaml'
SPEC_FILE_PATH = os.getcwd() + os.path.sep + SPEC

SPEC_DICT = None
SPECIFICATION = None

PROJECT_OUTPUT = os.getcwd() + os.path.sep + 'generated'
SERVER_OUTPUT = PROJECT_OUTPUT + os.path.sep + 'server'

USER_TEMPLATES_NAME = None
USER_TEMPLATES_PATH = None

DEFAULT_TEMPLATES_DIR = 'templates'
