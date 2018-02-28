"""
How would a multi-specification project look like?

Our single-specification structure currently:
project/            codegen/
    spec1/              codegen/
    setup.py            setup.py
    ...                 ...

Would multi-specification look like this?:
project/            Are files shared between them or are they more or less independent apps?
    spec1/
    spec2/
    spec3/
    setup.py
    ...

Iterators will remain the same across languages, though more iterators can be added.
Only enclosed functions would differ between languages (translation package)

Codegen flow?:
1.  Iterate over spec and pass subtree and user-config parameters into iterator's functions

2   Functions need to use templates/libraries to return a usable working template in some form?
    These enclosed functions would all need to follow the same structure (parameters and return if applicable)
    Ex. all functions would be called as: f1(data, params) 
    params is needed to know where to place files
    Clarification on how classes would be beneficial? Function signatures can specify to only accept certain types?

3.  Process templates and parameters to actually generate files in correct locations

Does order matter for these iterators?

The enclosed functions receive subtrees, so 
we're likely going to have to do some preprocessing to ensure that the subtree is not dependent on other parts of the specification
"""


def invocation_iterator(invocation_functions):
    pass
    # creates root project directory (outermost 'codegen' folder) details such as 'setup.py' 'requirements.txt'
    # this phase likely only requires user parameters (config)


def specification_iterator(Specification_functions):
    pass
    # creates app/api directory details such as base files(models, encoder, deserializer), __init__.py, __main__.py, servers and ports


def schemas_iterator(schemas_functions):
    pass
    # deals with outputting each individual model file
