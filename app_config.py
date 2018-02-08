# LANGUAGES AND FRAMEWORKS CURRENTLY SUPPORTED
valid_server_targets = ['python-flask', 'nodejs']
valid_client_targets = ['python', 'javascript']

# DEFAULT VALUES THAT CAN BE CHANGED BY USER
SPEC_FILES = ['sample/sample.yaml']
CAMEL_CASE = True
SNAKE_CASE = False

# choose from valid_server_targets and valid_client_targets
SERVER_TARGET = 'python-flask'
CLIENT_TARGET = 'python'

# we can either have these in the config file or hide this in the main code
FLASK_TEMPLATES_DIR = 'templates/flask/'
FLASK_MODEL_TEMPLATE_PATH = FLASK_TEMPLATES_DIR + 'model.template'
FLASK_X_TEMPLATE_PATH = FLASK_TEMPLATES_DIR + 'x.template'

NODEJS_TEMPLATES_DIR = 'templates/nodejs/'
NODEJS_MODEL_TEMPLATE_PATH = NODEJS_TEMPLATES_DIR + 'model.template'
NODEJS_X_TEMPLATE_PATH = NODEJS_TEMPLATES_DIR + 'x.template'
