# Depends on if we have one big codegen module including each language
# or we do a core module and several different language-specific modules
# will client side code generation have to be separate modules as well?
# unrelated code (ex. flask and nodejs) will be stored together, which doesn't seem efficient

# LANGUAGES AND FRAMEWORKS CURRENTLY SUPPORTED
# valid_server_targets = ['python-flask', 'nodejs']
# valid_client_targets = ['python', 'javascript']

# PARTS OF CODEGEN ABLE TO BE SUPPRESSED
# valid_suppress_targets = []

# don't let user choose for certain files
SUPPRESSIBLE = ['Schemas', 'Responses', 'Examples',
                'RequestBodies', 'Headers', 'SecuritySchemes']

# Allows user to change filenames
# Base directory default includes: requirements.txt, README.md, setup.py, server code directory
# should maybe allow user to specify a path here? to generate files into a premade folder
BASE_DIR_NAME = 'python-flask-server-generated'

# Server code directory default includes: api code directories, __init__.py, __main__.py, encoder.py, util.py?
SERVER_CODE_DIR_NAME = 'server'
CONTROLLERS_DIR_NAME = 'controllers'
MODELS_DIR_NAME = 'models'
SPEC_DIR_NAME = 'spec'

# we would need something to let user change where code is generated to?
OUTPUT_DIR_STRUCTURE = [
    {
        SERVER_CODE_DIR_NAME: [
            {
                CONTROLLERS_DIR_NAME: [
                    # not sure what kind of code we want to give the option to move around?
                ]
            },
            {
                MODELS_DIR_NAME: [

                ]
            },
            {
                SPEC_DIR_NAME: [

                ]
            }
        ]
    },
    'README.md',
    'requirements.txt',
    'setup.py'
]

# DEFAULT VALUES THAT CAN BE CHANGED BY USER
SPEC_FILES = ['sample/sample.yaml']
CAMEL_CASE = True
SNAKE_CASE = False
SUPPRESS = []

# choose from valid_server_targets and valid_client_targets
# SERVER_TARGET = 'python-flask' # unneeded if we do separate modules for different languages
CLIENT_TARGET = 'python'

# we can either have these in the config file or hide this in the main code
# FLASK_TEMPLATES_DIR = 'templates/server/flask/'
# FLASK_MODEL_TEMPLATE_PATH = FLASK_TEMPLATES_DIR + 'model.template'
# FLASK_X_TEMPLATE_PATH = FLASK_TEMPLATES_DIR + 'x.template'

# NODEJS_TEMPLATES_DIR = 'templates/server/nodejs/'
# NODEJS_MODEL_TEMPLATE_PATH = NODEJS_TEMPLATES_DIR + 'model.template'
# NODEJS_X_TEMPLATE_PATH = NODEJS_TEMPLATES_DIR + 'x.template'
