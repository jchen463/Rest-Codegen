"""
Minimal structure and strictness
user will have to import our default_codegen module to use codegen_stage()
"""
import codegen.default_codegen as default  # import will look like this because codegen will be a package
# i/mport default_codegen as default   # use this if just testing within the files
import codegen.codegen_config as cfg

SPEC = 'swagger.yaml'
LANGUAGE = 'flask'
PROJECT_NAME = 'myproject'
# TEMPLATES_DIR = 'templates'


def my_iterator(spec, my_iterator_functions):
    print('starting my iterator')
    dikt = {}
    for f in my_iterator_functions:
        f(dikt)


def function1(dikt):
    print('function1')
    # emits file defined by template of user
    # the template specified by the first argument is the user's defined template from the location of where user calls codegen from
    # the 3rd argument is the directory they want to output it to
    # suppresses all files that codegen genenerates with the template 'init.tmpl'
    default.emit_template("templates/flask_server/init.tmpl", dikt, cfg.FLASK_PROJECT_NAME + "/flask_server", "my_init.py")

# def my_controllers_function(params):
#     print("starting my function using codegen's paths_iterator")

#     for path in params:
#         path['url'] = path['url'].replace('{', '<').replace('}', '>')

#     dikt = {
#         'paths_list': params
#     }
#     # emits file defined by template of user and supresses all the codegen's generated files using the name "controller.tmpl"
#     default.emit_template("templates/flask_server/controller.tmpl", dikt, cfg.FLASK_PROJECT_NAME + "/flask_server", "controllers/my_controller.py")


def function2(dikt):
    print('function2')


def main():
    my_iterator_functions = [
        function1,
        function2,
    ]

    default.codegen_stage(my_iterator, my_iterator_functions)
    # default.codegen_stage(default.paths_iterator, [my_controllers_function])


main()
