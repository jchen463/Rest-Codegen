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
# maps the type in OpenApi3 to the type in python
# types: [array, boolean, integer, null,  number, object, string]
# formats that matter for strings: ByteArray, Binary, date, datetime

typeMapping = {
    'integer': 'number', 'long': 'number', 'float': 'number', 'double': 'number',
    'string': 'string', 'byte': 'string', 'binary': 'string', 'boolean': 'boolean',
    'date': 'string', 'date-time': 'string', 'password': 'string', 'object': 'any'
}


def typescript_project_setup():
    print('typescript_project_setup')
    # default.emit_template('requirements.j2', dikt, cfg.TYPESCRIPT_PROJECT_OUTPUT, 'requirements.txt')


def typescript_specification_setup():
    # dikt = params
    # params contains 'tags', 'models
    print('typescript_specfication_setup')
    default.emit_template('typescript_client/index.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT, 'index.ts')
    default.emit_template('typescript_client/variables.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT, 'variables.ts')
    default.emit_template('typescript_client/configuration.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT, 'configuration.ts')
    default.emit_template('typescript_client/api_ts.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT + os.path.sep + 'api', 'api.ts')
    # dikt['models'] = [makeFirstLetterLower(s) for s in dikt['models']]
    default.emit_template('typescript_client/models.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT + os.path.sep + 'model', 'models.ts')
    default.emit_template('typescript_client/encoder.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT, 'encoder.ts')
    default.emit_template('typescript_client/api_module.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT, 'api.module.ts')
    default.emit_template('typescript_client/rxjs.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT, 'rxjs-operators.ts')


def typescript_generate_service():  # params is an array of dictionaries
    # CHECK notes/servicetemplatesnodes.ts for TODO
    # almost done
    """
    [
        {
            'url': ,
            'method': ,
            'tag': ,
            'properties': OperationObject,
            'basePath': ,
            'in': ,
            'contents': ,
            'request_bodies': ,
            'param_to_type': ,
            'observable: ,
            'request_body_type': ,
        },
        {

        },
    ]
    """
    dependencies = []
    base_path = ''
    base_path = params[0]['basePath']
    name = ''
    for path in params:
        path['url'] = path['url'].replace('{', '${encodeURIComponent(String(').replace('}', '))}')
        param_to_type = {}
        param_to_short_type = {}
        observable = '{}'
        path['in'] = []
        # this breaks if parameters are references
        if path['properties'].parameters is not None:
            for parameter in path['properties'].parameters:
                param_to_type[parameter.name] = get_parameter_type(parameter)
                if parameter._in not in path['in']:
                    path['in'].append(parameter._in)
        path['param_to_type'] = param_to_type
        path['contents'] = ['application/json', 'application/xml']
        path['observable'] = get_observable(path['properties'].responses)
        get_dependencies(dependencies, path['properties'].responses)
        for status_code, response in path['properties'].responses.items():
            if response.content is not None:
                path['contents'] = []
                for content_name, mediatype_obj in response.content.items():
                    if content_name not in path['contents']:
                        path['contents'].append(content_name)

                    """
                    Not sure if there's a better way to fetch dependencies
                    They're stored under each response.
                    """

                    # if mediatype_obj.schema is not None:
                    #     if mediatype_obj.schema.ref is not None:
                    #         name = mediatype_obj.schema.ref.split('/')[3]
                    #         if name not in dependencies:
                    #             dependencies.append(name)
                    #     if mediatype_obj.schema.type == 'array':
                    #         if mediatype_obj.schema.items.ref is not None:
                    #             name = mediatype_obj.schema.items.ref.split('/')[3]
                    #             if name not in dependencies:
                    #                 dependencies.append(name)

        if path['properties'].parameters is None:
            path['properties'].parameters = []

    for i in range(len(dependencies)):
        dependencies[i] = [dependencies[i], makeFirstLetterLower(dependencies[i])]

    # print(dependencies)

    dikt = {
        'paths_list': params,
        'base_path': base_path,
        'dependencies': dependencies,
    }

    default.emit_template('typescript_client/service.j2', dikt, cfg.TYPESCRIPT_PROJECT_OUTPUT + os.path.sep + 'api', params[0]['tag'] + '.service.ts')


def get_dependencies(dependencies, responses_dict):
    if '200' not in responses_dict:
        return
    if responses_dict['200'].content is None:
        return
    for content_type, content_obj in responses_dict['200'].content.items():
        if content_obj.schema is not None:
            append_dependencies(dependencies, content_obj.schema)

# DEPENDS ON SCHEMAS BEING STORED AS REFERENCES


def append_dependencies(dependencies, schema_obj):
    ref = getattr(schema_obj, 'ref', None)
    if ref is not None:
        ref = ref.split('/')[3]
        if ref not in dependencies:
            dependencies.append(ref)
        return
    if schema_obj.type == 'array':
        append_dependencies(dependencies, schema_obj.items)
    return


def get_observable(responses_dict):
    observable_str = '{}'
    if '200' not in responses_dict:
        return observable_str
    if responses_dict['200'].content is None:
        return observable_str
    for content_type, content_obj in responses_dict['200'].content.items():
        if content_obj.schema is not None:
            observable_str = get_observable_type_string(content_obj.schema, 0)
        break
    return observable_str


def get_observable_type_string(schema_obj, depth):
    ref = getattr(schema_obj, 'ref', None)
    if ref is not None:
        s = ref.split('/')[3]
        for x in range(depth):
            s += '>'
        return s
    if schema_obj.type == 'array':
        return 'Array<' + get_observable_type_string(schema_obj.items, depth + 1)
    s = typeMapping[schema_obj.type]
    for x in range(depth):
        s += '>'
    return s


def get_parameter_type(parameter_obj):
    type_str = 'any'

    if parameter_obj.schema is not None:
        type_str = get_type_string(parameter_obj.schema, 0)

    return type_str


def get_type_string(schema_obj, depth):
    if schema_obj.type == 'array':
        return 'Array<' + get_type_string(schema_obj.items, depth + 1)
    else:
        s = typeMapping[schema_obj.type]
        for x in range(depth):
            s += '>'
        return s

def getTypeScriptType(attribute, model, attribute_name):
    typescript_type = ""

    if 'ref' in attribute.__dict__:
        typescript_type += attribute.ref[attribute.ref.rfind('/') + 1:]  # reference name wil lbe the name of the type
        # if the class has not been added to the dependencies, add it
        if makeFirstLetterLower(typescript_type) not in model['dependencies']:
            model['dependencies'][makeFirstLetterLower(typescript_type)] = typescript_type
    elif attribute.type == 'array':
        tempAttr = attribute.items
        typescript_type += 'Array<'
        array_num = 1  # count the number of arrays found

        # untested while loop
        while hasattr(tempAttr, 'type'):
            if tempAttr.type == 'array':
                typescript_type += 'Array<'
                tempAttr = tempAttr.items
                array_num += 1
            else:
                break

        if 'ref' in tempAttr.__dict__:
            typescript_type += tempAttr.ref[tempAttr.ref.rfind('/') + 1:]

            # if the class has not been added to the dependencies, add it
            if makeFirstLetterLower(tempAttr.ref[tempAttr.ref.rfind('/') + 1:]) not in model['dependencies']:
                model['dependencies'][makeFirstLetterLower(tempAttr.ref[tempAttr.ref.rfind('/') + 1:])] = \
                    tempAttr.ref[tempAttr.ref.rfind('/') + 1:]
        elif tempAttr.type == 'string':
            model['properties'][attribute_name]['isString'] = True
            if not tempAttr.enum:
                if tempAttr.format:
                    typescript_type += typeMapping[tempAttr.format]
                else:
                    typescript_type += typeMapping[tempAttr.type]
            else:  # is enum so you have to print something different
                typescript_type += model['name'].capitalize() + "." + attribute_name.capitalize() + "Enum"
                model['enums'][attribute_name] = tempAttr.enum

        elif tempAttr.type in typeMapping:
            typescript_type += typeMapping[tempAttr.type]

        for _ in range(array_num):
            typescript_type += '>'

            # untested while loop:
            # while attribute.items.type
            # attribute_type = '[]' # this will need to be fixed
    elif attribute.type == 'string':
        model['properties'][attribute_name]['isString'] = True
        if not model['properties'][attribute_name]['enum']:
            if attribute.format:
                typescript_type += typeMapping[attribute.format]
            else:
                typescript_type += typeMapping[attribute.type]
        else:  # is enum so you have to print something different
            typescript_type += model['name'].capitalize() + "." + attribute_name.capitalize() + "Enum"
            model['enums'][attribute_name] = model['properties'][attribute_name]['enum']
    else:  # attribute.type == integer
        typescript_type = typeMapping[attribute.type]

    return typescript_type


def typescript_models_setup():
    # model files
    print('typescript_models_setup')

    default.emit_template('typescript_client/model.j2', cfg.TEMPLATE_VARIABLES, cfg.TYPESCRIPT_PROJECT_OUTPUT +
                            os.path.sep + 'model', makeFirstLetterLower(cfg.TEMPLATE_VARIABLES['_current_schema']) + '.ts')

    pass

def makeFirstLetterLower(s):
    return s[:1].lower() + s[1:] if s else ''


typescript_invocation_iterator_functions = [
    typescript_project_setup,
]

typescript_specification_iterator_functions = [
    typescript_specification_setup
]

typescript_paths_iterator_functions = [
    typescript_generate_service,
]

typescript_schemas_iterator_functions = [
    typescript_models_setup,
]


def stage_default_iterators():
    default.codegen_stage(default.invocation_iterator, typescript_invocation_iterator_functions)
    default.codegen_stage(default.specification_iterator, typescript_specification_iterator_functions)
    default.codegen_stage(default.schemas_iterator, typescript_schemas_iterator_functions)
    default.codegen_stage(default.paths_iterator, typescript_paths_iterator_functions)


def typescript_client_codegen():
    default.run_iterators()
