"""
Minimal structure and strictness
We're going to have to load this twice if specification stays in here
"""
import default_codegen

SPECIFICATION = 'sample.yaml'
PROJECT_OUTPUT_DIR = 'myproject'


def my_iterator(my_iterator_functions):
    print('starting my iterator')


def function1():
    print('function1')


def function2():
    print('function2')


def main():
    my_iterator_functions = [
        function1,
        function2,
    ]

    default_codegen.codegen_stage(my_iterator, my_iterator_functions)
    default_codegen.codegen_stage(default_codegen.invocation_iterator, [])


main()
