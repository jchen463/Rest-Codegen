import codegen.default_codegen as default
from codegen.main2 import load_build_file


def flask_project_setup(dikt):
    pass


def flask_api_setup(dikt):
    pass


def flask_controllers_setup(dikt):
    pass


def flask_models_setup(dikt):
    pass


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
    default.codegen_stage(default.invocation_iterator, flask_invocation_iterator_functions)
    default.codegen_stage(default.specification_iterator, flask_specification_iterator_functions)
    default.codegen_stage(default.schemas, flask_schemas_iterator_functions)
    default.codegen_stage(default.paths_iterator, flask_paths_iterator_functions)


def run_iterators():
    for iterator_name, iterator in default.iterators_mapping:
        iterator(default.iterator_functions_mapping[iterator_name])


def flask_server_codegen(spec_dict, build_file):
    stage_default_iterators()
    load_build_file(build_file)
    run_iterators(spec_dict)