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

def typescript_project_setup(dikt):
    print('typescript_project_setup')
    default.emit_template('requirements.tmpl', dikt, cfg.PROJECT_OUTPUT, 'requirements.txt')

 
def typescript_specification_setup(dikt):
    default.emit_template('typescript_client/index.tmpl', dikt, cfg.PROJECT_OUTPUT, 'index.ts')
    default.emit_template('typescript_client/variables_client.tmpl', dikt, cfg.PROJECT_OUTPUT, 'variables.ts')
    default.emit_template('typescript_client/configuration.tmpl', dikt, cfg.PROJECT_OUTPUT, 'configuration.ts')
   

def typescript_api_setup(dikt):
    # controller files
    # dikt contains 'paths'
    # print('typescript_controllers_setup')
    # # for url, _ in dikt['paths'].items():
    # #    dikt['paths']['url']
    # tags = {'tags': [] }

    # # for tag in spec_dict['tags']:
    # #     tags['tags'].append(tag['name'])
    # new_dikt = {}

    # for key, value in dikt:
    #     new_dikt[key] = value

    print(dikt['url'])
    print(dikt['paths'])

    # controller_dep = {
    #     'dependencies': [
    #         {'location': '@angular/core', 'objects': ['Inject', 'Injectable', 'Optional'] },
    #         {'location': '@angular/http', 'objects': ['Http', 'Headers', 'URLSearchParams'] },
    #         {'location': '@angular/http', 'objects': ['RequestMethod', 'RequestOptions', 'RequestOptionsArgs'] },
    #         {'location': '@angular/http', 'objects': ['Response, ResponseContentType']},
    #         {'location': 'rxjs/Observable', 'objects': ['Observable']},
    #         {'location': '../variables', 'objects': ['BASE_PATH', 'COLLECTION_FORMATS']},
    #         {'location': '../configuration', 'objects': ['Configuration']}
    #     ]
    # }

    # for tag in tags['tags']:
    #     file_name = tag.capitalize() + 'Api.ts'
    #     tag = {'tag': tag}
    #     # renders = [FileRender('templates/client_api.tmpl', file_name,
    #     #                       [controller_dep, tags, controller_functions, methods, basePath])]
    #     default.emit_template('typescript_client/api.tmpl', dikt, cfg.PROJECT_OUTPUT, capitalize(tag) + 'Api.ts')


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

def flask_server_codegen():
    default.run_iterators()

