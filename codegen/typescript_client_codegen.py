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

def typescript_project_setup(params):
    print('typescript_project_setup')
    dikt = {}
    default.emit_template('requirements.tmpl', dikt, cfg.PROJECT_OUTPUT, 'requirements.txt')

 
def typescript_specification_setup(params):
    dikt = {}
    default.emit_template('typescript_client/index.tmpl', dikt, cfg.PROJECT_OUTPUT, 'index.ts')
    default.emit_template('typescript_client/variables.tmpl', dikt, cfg.PROJECT_OUTPUT, 'variables.ts')
    default.emit_template('typescript_client/configuration.tmpl', dikt, cfg.PROJECT_OUTPUT, 'configuration.ts')
   
type_map = {'integer': 'number', 'string': 'string', 'array': 'Array', 'boolean': 'boolean' }

def typescript_api_setup(params):
    print('typescript_controllers_setup')
    basePath = params[0]['basePath']
    dikt = { 'basePath': basePath, 'paths': [], 'tag': params[0]['tag']}

    # get the arguments
    for path in params:
        newPathDic = { 'url': path['url'], 'parameters' : [], 'properties': path['properties'], 'method': path['method']}
        # GET THE ARGUMENTS 
        if newPathDic['properties'].parameters is not None:
            # print(path['properties'].parameters)
            if path['properties'].parameters is not None:
                for param in path['properties'].parameters: 
                    #print(param.name)
                    newArg = param.name
                    if param.schema.type == 'array':
                        #print(param.required)
                        if param.required == False:
                            newArg += "?"
                        newArg += ": Array<" + type_map[param.schema.items.type] + ">"
                    else: 
                        if param.required == False:
                            newArg += "?"
                        newArg += ": " + type_map[param.schema.type]
                    newPathDic['parameters'].append(newArg)
        if path['properties'].requestBody is not None:
            if 'ref' in path['properties'].requestBody.__dict__:
                refPath = path['properties'].requestBody.ref
                splitPath = refPath.split('/')
                newArg = "body: models." + splitPath[len(splitPath) - 1].capitalize()
                newPathDic['parameters'].append(newArg)
            elif 'content' in path['properties'].requestBody.__dict__:
                if 'application/x-www-form-urlencoded' in path['properties'].requestBody.content:
                    for key, value in path['properties'].requestBody.content['application/x-www-form-urlencoded'].schema.properties.items():
                        newArg = key + "?: "
                        if value.type == 'array':
                            newArg += "Array<" + type_map[value.schema.items.type] + ">"
                        else: 
                            newArg += type_map[value.type]
                        newPathDic['parameters'].append(newArg)
                elif 'application/json' in path['properties'].requestBody.content:
                    refPath = path['properties'].requestBody.content['application/json'].schema.ref
                    splitPath = refPath.split('/')
                    newArg = "body: models." + splitPath[len(splitPath) - 1].capitalize()
                    newPathDic['parameters'].append(newArg)
                elif 'application/octet-stream' in path['properties'].requestBody.content:
                    newArg = "additionalMetadata?: " + path['properties'].requestBody.content['application/octet-stream'].schema.type
                    newPathDic['parameters'].append(newArg)
                    newArg = "file?: any"
                    newPathDic['parameters'].append(newArg)
        # GET THE OBSERVABLE PARAM
            if '200' in path['properties'].responses:
                if 'content' in path['properties'].responses['200'].__dict__:
                    #print(path['properties'].responses['200'].content)
                    if 'application/json' in path['properties'].responses['200'].content:
                        if 'schema' in path['properties'].responses['200'].content['application/json'].__dict__:
                            for key, value in path['properties'].responses['200'].content['application/json'].__dict__.items():
                                if key == 'schema':
                                    if 'ref' in value.__dict__:
                                        refPath = value.ref
                                        splitPath = refPath.split('/')
                                        response_200 = "models." + splitPath[len(splitPath) - 1]
                                    elif 'type' in value.__dict__:
                                        if value.type == 'array':
                                            if 'ref' in value.items:
                                                refPath = value.ref
                                                splitPath = refPath.split('/')
                                                response_200 = "<Array<models." + splitPath[len(splitPath) - 1] + ">"
                                    newPathDic.update({ 'response_200': response_200})
                                    #print(newPathDic['response_200'])
        dikt['paths'].append(newPathDic)
        print(path['properties'].operationId)
        print(newPathDic['parameters'])
    default.emit_template('typescript_client/api.tmpl', dikt, cfg.PROJECT_OUTPUT + os.path.sep + 'api', params[0]['tag'].capitalize() + 'Api' + '.ts')


# returns the python type and if needed, adds libraries/dependencies
def getTypeScriptType(attribute, model):
    # maps the type in OpenApi3 to the type in python
        # types: [array, boolean, integer, null,  number, object, string]
        # formats that matter for strings: ByteArray, Binary, date, datetime
    typeMapping = {
        'integer': 'number', 'long': 'number', 'float': 'number', 'double': 'number',
        'string': 'string', 'byte': 'string', 'binary': 'string', 'boolean': 'boolean',
        'date': 'string', 'date-time': 'string', 'password': 'string', 'object': 'any'
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
            if tempAttr.format:
                python_type += typeMapping[tempAttr.format]
            else:
                python_type += typeMapping[tempAttr.type]
        elif tempAttr.type in typeMapping:
            python_type += typeMapping[tempAttr.type]

        for _ in range(array_num):
            python_type += '>'

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

def typescript_models_setup(schema):
    # model files
    print('typescript_models_setup')

    model = {
        'name': schema['name'],
        'properties': {},  # key is property name, value is property type
        'dependencies': {}  # key is filename, value is class that is being imported

    }

    class_name = makeFirstLetterLower(model['name'])

    # if properties does not exist, print an empty class
    if not schema['object'].properties:
        default.emit_template('model.tmpl', model, cfg.PROJECT_OUTPUT +
                              os.path.sep + 'models', class_name + '.py')
    else:
        # run through each item within the properties
        for attribute_name, attribute in schema['object'].properties.items():

            # find the property, and insert dependencies into the model if needed
            attribute_type = getTypeScriptType(attribute, model)

            # if attribute type is null or empty do not include it into the dictionary
            if attribute_type != "" and attribute_type != 'null':
                model['properties'][attribute_name] = attribute_type

        default.emit_template('typescript_client/model.tmpl', model, cfg.PROJECT_OUTPUT +
                              os.path.sep + 'models', class_name + '.ts')


    pass
    # for schema_name, schema_info in dikt['schemas'].items():
    #     dikt['schemas']['schema_name']

    # type_map = {'integer': 'number', 'string': 'string', 'array': None, 'boolean': 'boolean' }

    # for key, value in spec_dict['components']['schemas'].items():

    #     models = {'model_name': key,
    #             'properties': [],
    #             'required': value['required']}

    #     for attribute, attribute_type in value['properties'].items():
    #         name = attribute
    #         if 'type' in attribute_type:
    #             if attribute_type['type'] != 'array':
    #                 val_type = attribute_type['type']
    #                 var_type = type_map[val_type]
    #             else:
    #                 if 'type' in attribute_type['items']:
    #                     item = attribute_type['items']['type']
    #                     var_type = 'Array<' + type_map[item] +'>'
    #                 elif '$ref' in attribute_type['items']:
    #                     item = attribute_type['items']['$ref']
    #                     var_type = 'Array<' + item +'>'
    #                 else: 
    #                     var_type = 'Array<' + 'None' + '>'
    #         else:
    #             var_type = 'none'
            
    #         if '$ref' in attribute_type:
    #             ref = attribute_type['$ref']
    #         else:
    #             ref = 'none'
            
    #         if 'enum' in attribute_type:
    #             enum = attribute_type['enum']

    #         new_attribute = { 'name': name, 'type': var_type, 'ref': ref, 'enum': enum }
    #         models['properties'].append(new_attribute)

    #     file_name = key + '.ts'
    #     model_name = {'model_name': key}
    #     renders = [FileRender('templates/client_models.tmpl', file_name, [models])]
    #     do_renders(renders, 'templates/', 'generated/client/models')

def makeFirstLetterLower(s):
    return s[:1].lower() + s[1:] if s else ''

def typescript_generate_models_ts(params):
    # params contains 'tags', 'models
    print("typescript_generate_models_ts")
    dikt = params
    dikt['models'] = [makeFirstLetterLower(s) for s in dikt['models']]
    default.emit_template('typescript_client/models.tmpl', dikt, cfg.PROJECT_OUTPUT + os.path.sep + 'models', 'models.ts')

def typescript_generate_api_ts(params):
    # params contains 'tags', 'models
    print("typescript_generate_api_ts")
    dikt = params
    default.emit_template('typescript_client/api_ts.tmpl', dikt, cfg.PROJECT_OUTPUT + os.path.sep + 'api', 'api.ts')

typescript_invocation_iterator_functions = [
    typescript_project_setup,
]

typescript_specification_iterator_functions = [
    typescript_specification_setup,
    typescript_generate_models_ts,
    typescript_generate_api_ts
]

typescript_paths_iterator_functions = [
    typescript_api_setup,
]

typescript_schemas_iterator_functions = [
    typescript_models_setup,
]


def stage_default_iterators():
    default.codegen_stage(default.invocation_iterator,
                          typescript_invocation_iterator_functions)
    default.codegen_stage(default.specification_iterator,
                          typescript_specification_iterator_functions)
    default.codegen_stage(default.schemas_iterator,
                          typescript_schemas_iterator_functions)
    default.codegen_stage(default.paths_iterator,
                          typescript_paths_iterator_functions)

def typescript_client_codegen():
    default.run_iterators()

