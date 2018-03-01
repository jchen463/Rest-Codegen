from default_codegen import codegen_stage
import default_codegen as d


def my_iterator(my_iterator_functions):
    print('starting my iterator')


def function1():
    print('function1')


def function2():
    print('function2')


my_iterator_functions = [
    function1,
    function2,
]

d.codegen_stage(my_iterator, my_iterator_functions)
d.codegen_stage(d.invocation_iterator, [])
