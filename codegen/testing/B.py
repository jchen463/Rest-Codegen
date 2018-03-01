import A

SPECIFICATION = 'sample.yaml'
PROJECT_OUTPUT_DIR = 'myproject'


def my_iterator(my_iterator_functions):
    print('starting my iterator')
    for f in my_iterator_functions:
        f()


def function1():
    print('function1')


def function2():
    print('function2')


def main():
    my_iterator_functions = [
        function1,
        function2,
    ]

    A.codegen_stage(my_iterator, my_iterator_functions)
