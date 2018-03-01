import os
import codegen.default_codegen as default
import importlib.util


def flask_project_setup(dikt):
    print('flask_project_setup')


def flask_api_setup(dikt):
    print('flask_api_setup')


def flask_controllers_setup(dikt):
    print('flask_controllers_setup')


def flask_models_setup(dikt):
    print('flask_models_setup')


flask_invocation_iterator_functions = [
    flask_project_setup,
]

flask_specification_iterator_functions = [
    flask_api_setup,
]

flask_paths_iterator_functions = [
    flask_models_setup,
]

flask_schemas_iterator_functions = [
    flask_controllers_setup,
]


def stage_default_iterators():
    default.codegen_stage(default.invocation_iterator,
                          flask_invocation_iterator_functions)
    default.codegen_stage(default.specification_iterator,
                          flask_specification_iterator_functions)
    default.codegen_stage(default.schemas_iterator,
                          flask_schemas_iterator_functions)
    default.codegen_stage(default.paths_iterator,
                          flask_paths_iterator_functions)


def run_iterators(spec_dict):
    for iterator_name, iterator in default.iterators_mapping.items():
        iterator(spec_dict, default.iterator_functions_mapping[iterator_name])


def flask_server_codegen(spec_dict, build_file):
    stage_default_iterators()

    # Stages user-defined iterators
    cwd = os.getcwd()
    full_path = cwd + '/' + build_file
    spec = importlib.util.spec_from_file_location(
        build_file[:-3], full_path)
    build_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build_script)

    run_iterators(spec_dict)
