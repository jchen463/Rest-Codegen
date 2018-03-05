"""
Minimal structure and strictness
user will have to import our default_codegen module to use codegen_stage()
"""
import codegen.default_codegen as default  # import will look like this because codegen will be a package
# import default_codegen as default   # use this if just testing within the files

SPEC = 'sample.yaml'
PROJECT_OUTPUT = 'myproject'
TEMPLATES_DIR = 'templates'


def my_iterator(spec, my_iterator_functions):
    print('starting my iterator')
    dikt = {}
    for f in my_iterator_functions:
        f(dikt)


def function1(dikt):
    print('function1')


def function2(dikt):
    print('function2')


def main():
    my_iterator_functions = [
        function1,
        function2,
    ]

    default.codegen_stage(my_iterator, my_iterator_functions)
    # default.codegen_stage(default_codegen.invocation_iterator, [])


main()
