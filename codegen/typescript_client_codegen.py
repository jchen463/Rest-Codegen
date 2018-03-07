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


def typescript_models_setup(dikt):
    # model files
    # dikt contains 'schemas'
    print('typescript_models_setup')
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
    dikt = params
    dikt['models'] = [makeFirstLetterLower(s) for s in dikt['models']]
    default.emit_template('typescript_client/models.tmpl', dikt, cfg.PROJECT_OUTPUT + os.path.sep + 'models', 'models.ts')

def typescript_generate_api_ts(params):
    # params contains 'tags', 'models
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

