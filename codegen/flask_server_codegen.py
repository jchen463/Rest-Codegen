import os
import importlib.util

try:  # when just doing $ python3 main.py only below imports work
    import codegen.default_codegen as default
    import codegen.codegen_config as cfg
except ImportError as err:  # when packaged, only above imports work
    import default_codegen as default
    import codegen_config as cfg

"""
These are essentially wrappers for templates
Responsible for certain files
"""


def flask_project_setup(params):
    # outer codegen folder: setup.py, requirements.txt. Dockerfile
    # params contains 'info', 'externalDocs'
    dikt = {}

    print('flask_project_setup')
    default.emit_template('requirements.tmpl', dikt, cfg.PROJECT_OUTPUT, 'requirements.txt')
    # default.emit_template('setup.tmpl', params, cfg.PROJECT_OUTPUT, 'setup.py')


def flask_api_setup(params):
    # inner codegen folder: base classes, encoder, deserializer. ???
    # params is the specification class

    dikt = {}  # access keys in templates

    print('flask_api_setup')
    default.emit_template('init.tmpl', dikt, cfg.PROJECT_OUTPUT, '__init__.py')
    # default.emit_template('main.tmpl', dikt, cfg.PROJECT_OUTPUT, '__main__.py')
    default.emit_template('encoder.tmpl', dikt, cfg.PROJECT_OUTPUT, 'encoder.py')
    default.emit_template('util.tmpl', dikt, cfg.PROJECT_OUTPUT, 'util.py')
    default.emit_template('base_model.tmpl', dikt, cfg.PROJECT_OUTPUT + os.path.sep + 'models', 'base_model_.py')


def flask_generate_controller(params):
    # controller files
    """
    params = 
    [
        {
            'url': ,
            'method': ,
            'tag': ,
            'properties': ,
        },
        {

        },
    ]
    """
    print('flask_controllers_setup')

    dikt = {
        'paths_list': params 
    }

    default.emit_template('controller.tmpl', dikt, cfg.PROJECT_OUTPUT + os.path.sep + 'controllers', params[0]['tag'] + '_controller' + '.py')



# returns the python type and if needed, adds libraries/dependencies
def getPythonType(attribute, model):
    # maps the type in OpenApi3 to the type in python
        #types: [array, boolean, integer, null,  number, object, string]
        #formats that matter for strings: ByteArray, Binary, date, datetime
    typeMapping = {
        'integer': 'int', 'long': 'int', 'float': 'float', 'double': 'float',
        'string': 'str', 'byte': 'ByteArray', 'binary': 'Binary', 'boolean': 'bool',
        'date': 'date', 'date-time': 'datetime', 'password': 'str', 'object': 'object'
    }

    python_type = ""

    if 'ref' in attribute.__dict__:
        python_type += attribute.ref[attribute.ref.rfind('/') + 1:] # reference name wil lbe the name of the type
        # if the class has not been added to the dependencies, add it
        if makeFirstLetterLower(python_type) not in model['dependencies']:
            model['dependencies'][makeFirstLetterLower(python_type)] = python_type
    elif attribute.type == 'array':
        tempAttr = attribute.items
        python_type += 'List['
        array_num = 1 # count the number of arrays found

        # untested while loop
        while hasattr(tempAttr, 'type'):
            if tempAttr.type == 'array':
                python_type += 'List['
                tempAttr = tempAttr.items
                array_num += 1
            else:
                break

        if 'ref' in tempAttr.__dict__:
            python_type += tempAttr.ref[tempAttr.ref.rfind('/') + 1:]

            # if the class has not been added to the dependencies, add it
            if makeFirstLetterLower(tempAttr.ref[tempAttr.ref.rfind('/') + 1:]) not in model['dependencies']:
                model['dependencies'][makeFirstLetterLower(tempAttr.ref[tempAttr.ref.rfind('/') + 1:])] = \
                    tempAttr.ref[tempAttr.ref.rfind('/') + 1:]
        elif tempAttr.type == 'string':
            if tempAttr.format:
                python_type += typeMapping[tempAttr.format]
            else:
                python_type += typeMapping[tempAttr.type]
        elif tempAttr.type in typeMapping:
            python_type += typeMapping[tempAttr.type]

        for _ in range(array_num):
            python_type += ']'

            # untested while loop:
            # while attribute.items.type
            # attribute_type = '[]' # this will need to be fixed
    elif attribute.type == 'string':
        if attribute.format:
            python_type += typeMapping[attribute.format]
        else:
            python_type += typeMapping[attribute.type]
    elif attribute.type in typeMapping:
        python_type += typeMapping[attribute.type]

    return python_type

def makeFirstLetterLower(s):
    return s[:1].lower() + s[1:] if s else ''

def flask_generate_model(schema):

    model = {
        'name': schema['name'],
        'properties': {}, # key is property name, value is property type
        'dependencies': {} # key is filename, value is class that is being imported

    }

    class_name = makeFirstLetterLower(model['name'])

    # if properties does not exist, print an empty class
    if not schema['object'].properties:
        default.emit_template('model.tmpl', model, cfg.PROJECT_OUTPUT +
                              os.path.sep + 'models', class_name + '.py')
    else:
        #run through each item within the properties
        for attribute_name, attribute in schema['object'].properties.items():

            # find the property, and insert dependencies into the model if needed
            attribute_type = getPythonType(attribute, model)

            # if attribute type is null or empty do not include it into the dictionary
            if attribute_type != "" and attribute_type != 'null':
                model['properties'][attribute_name] = attribute_type

        default.emit_template('model.tmpl', model, cfg.PROJECT_OUTPUT +
                           os.path.sep + 'models', class_name + '.py')


flask_invocation_iterator_functions = [
    flask_project_setup,
]

flask_specification_iterator_functions = [
    flask_api_setup,
]

flask_paths_iterator_functions = [
    flask_generate_controller,
]

flask_schemas_iterator_functions = [
    flask_generate_model,
]


def stage_default_iterators():
    default.codegen_stage(default.invocation_iterator, flask_invocation_iterator_functions)
    default.codegen_stage(default.specification_iterator, flask_specification_iterator_functions)
    default.codegen_stage(default.schemas_iterator, flask_schemas_iterator_functions)
    default.codegen_stage(default.paths_iterator, flask_paths_iterator_functions)


def flask_server_codegen():
    default.run_iterators()
