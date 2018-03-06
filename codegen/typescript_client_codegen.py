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
        newPathDic = { 'url': path['url'], 'parameters' : [] , 'properties': path['properties'], 'method': path['method']}
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
            dikt['paths'].append(newPathDic)
    

        #if path['properties'].requestBody is not None:
            # for key, value in path['properties'].requestBody: 
            #     if path['properties'].requestBody.content is not None:
            #     print(path['properties'].requestBody.content)
            #     for key, value in path['properties'].requestBody.content.items():
            #         if (key == "application/x-www-form-urlencoded"):
            #             #for item, key in path['properties'].requestBody.content:
            #             newArg += value.schema.name
            #             newArg += type_map[value.schema.type]
            #         else:
            #             newArg = "body :"
            #     newPathDic['parameters'].append(newArg)

        #print(newPathDic['parameters'])
        #else:
            #if 
        #     print(paths['properties'][''])

            #print(params)
                #args.append( params.name + ":" str(params.schema.type) )
            #path.update(args[])

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


typescript_invocation_iterator_functions = [
    typescript_project_setup,
]

typescript_specification_iterator_functions = [
    typescript_specification_setup,
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

