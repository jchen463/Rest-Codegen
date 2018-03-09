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
    dikt = params
    print('flask_project_setup')
    default.emit_template('flask_server/requirements.tmpl', dikt, cfg.FLASK_PROJECT_OUTPUT, 'requirements.txt')
    # default.emit_template('flask_server/setup.tmpl', params, cfg.FLASK_PROJECT_OUTPUT, 'setup.py')


def flask_generate_base_model(params):
    dikt = {}
    default.emit_template('flask_server/base_model.tmpl', dikt, cfg.FLASK_SERVER_OUTPUT + os.path.sep + 'models', 'base_model.py')
    default.emit_template('flask_server/util.tmpl', dikt, cfg.FLASK_SERVER_OUTPUT, 'util.py')
    default.emit_template('flask_server/encoder.tmpl', dikt, cfg.FLASK_SERVER_OUTPUT, 'encoder.py')


def flask_generate_main(params):
    # params contains 'tags'
    dikt = params
    default.emit_template('flask_server/init.tmpl', dikt, cfg.FLASK_SERVER_OUTPUT, '__init__.py')
    default.emit_template('flask_server/main.tmpl', dikt, cfg.FLASK_SERVER_OUTPUT, '__main__.py')


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

    for path in params:
        path['url'] = path['url'].replace('{', '<').replace('}', '>')

    dikt = {
        'paths_list': params
    }

    default.emit_template('flask_server/controller.tmpl', dikt, cfg.FLASK_SERVER_OUTPUT + os.path.sep + 'controllers', params[0]['tag'] + '_controller' + '.py')


# returns the python type and if needed, adds libraries/dependencies
def getPythonType(attribute, model, attribute_name):
    # maps the type in OpenApi3 to the type in python
        # types: [array, boolean, integer, null,  number, object, string]
        # formats that matter for strings: ByteArray, Binary, date, datetime
    typeMapping = {
        'integer': 'int', 'long': 'int', 'float': 'float', 'double': 'float',
        'string': 'str', 'byte': 'ByteArray', 'binary': 'Binary', 'boolean': 'bool',
        'date': 'date', 'date-time': 'datetime', 'password': 'str', 'object': 'object'
    }

    python_type = ""

    if 'ref' in attribute.__dict__:
        python_type += attribute.ref[attribute.ref.rfind('/') + 1:]  # reference name wil lbe the name of the type
        # if the class has not been added to the dependencies, add it
        if makeFirstLetterLower(python_type) not in model['dependencies']:
            model['dependencies'][makeFirstLetterLower(python_type)] = python_type
    elif attribute.type == 'array':
        tempAttr = attribute.items
        python_type += 'Array<'
        array_num = 1  # count the number of arrays found

        # untested while loop
        while hasattr(tempAttr, 'type'):
            if tempAttr.type == 'array':
                python_type += 'Array<'
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
            model['properties'][attribute_name]['isString'] = True
            if not tempAttr.enum:
                if tempAttr.format:
                    python_type += typeMapping[tempAttr.format]
                else:
                    python_type += typeMapping[tempAttr.type]
            else:  # is enum so you have to print something different
                # python_type += model['name'].capitalize() +"." + attribute_name.capitalize() + "Enum"
                if tempAttr.format:
                    python_type += typeMapping[tempAttr.format]
                else:
                    python_type += typeMapping[tempAttr.type]
                model['enums'][attribute_name] = tempAttr.enum

        elif tempAttr.type in typeMapping:
            python_type += typeMapping[tempAttr.type]

        for _ in range(array_num):
            python_type += '>'

            # untested while loop:
            # while attribute.items.type
            # attribute_type = '[]' # this will need to be fixed
    elif attribute.type == 'string':
        model['properties'][attribute_name]['isString'] = True
        if not model['properties'][attribute_name]['enum']:
            if attribute.format:
                python_type += typeMapping[attribute.format]
            else:
                python_type += typeMapping[attribute.type]
        else:  # is enum so you have to print something different
            # python_type += model['name'].capitalize() + "." + attribute_name.capitalize() + "Enum"
            if attribute.format:
                python_type += typeMapping[attribute.format]
            else:
                python_type += typeMapping[attribute.type]
            model['enums'][attribute_name] = model['properties'][attribute_name]['enum']

    return python_type


def makeFirstLetterLower(s):
    return s[:1].lower() + s[1:] if s else ''


def flask_generate_model(schema):
    print('flask_generate_model')

    model = {
        'name': schema['name'],
        'properties': {},  # key is property name, value is property type
        'dependencies': {},  # key is filename, value is class that is being imported
        'required': schema['object'].required,
        'enums': {},  # Is this needed??1
        'isString': False  # is this needed??
    }

    class_name = makeFirstLetterLower(model['name'])

    # if properties does not exist, print an empty class, this may not ever even run since classes are always
    # initialized to empty arrays
    if not schema['object'].properties:
        default.emit_template('model.tmpl', model, cfg.TYPESCRIPT_PROJECT_OUTPUT +
                              os.path.sep + 'models', class_name + '.py')
    else:
        # run through each item within the properties
        for attribute_name, attribute in schema['object'].properties.items():
            model['properties'][attribute_name] = attribute.__dict__

            # find the property, and insert dependencies into the model if needed
            attribute_type = getPythonType(attribute, model, attribute_name)

            # if attribute type is null or empty do not include it into the dictionary
            if attribute_type != "" and attribute_type != 'null':
                model['properties'][attribute_name]['type'] = attribute_type

        default.emit_template('flask_server/model.tmpl', model, cfg.FLASK_SERVER_OUTPUT +
                              os.path.sep + 'models', class_name + '.py')


flask_invocation_iterator_functions = [
    flask_project_setup,
]

flask_specification_iterator_functions = [
    flask_generate_main,
    flask_generate_base_model,
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
