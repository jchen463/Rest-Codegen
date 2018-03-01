"""
Minimal structure and strictness
We're going to have to load this twice if specification stays in here
user will have to import our default_codegen module to use codegen_stage()
I think variable things, such as spec and project_output need to either be required or invoked via a function call
"""
import codegen.default_codegen

SPEC = 'swagger.yaml'
PROJECT_OUTPUT = 'myproject'


def my_iterator(my_iterator_functions):
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

    codegen.default_codegen.codegen_stage(my_iterator, my_iterator_functions)
    # default_codegen.codegen_stage(default_codegen.invocation_iterator, [])


main()
