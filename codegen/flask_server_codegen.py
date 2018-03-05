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
    default.emit_template('main.tmpl', dikt, cfg.PROJECT_OUTPUT, '__main__.py')
    default.emit_template('encoder.tmpl', dikt, cfg.PROJECT_OUTPUT, 'encoder.py')
    default.emit_template('util.tmpl', dikt, cfg.PROJECT_OUTPUT, 'util.py')
    default.emit_template('base_model.tmpl', dikt, cfg.PROJECT_OUTPUT + os.path.sep + 'models', 'base_model.py')


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


def flask_generate_model(params):
    # model files
    print('flask_models_setup')

    # default.emit_template('model.tmpl', params, cfg.PROJECT_OUTPUT +
    #                       os.path.sep + 'models', schema_name + '.py')


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
