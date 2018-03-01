iterators_mapping = {}
iterator_functions_mapping = {}


def codegen_stage(x_iterator, x_iterator_functions):
    iterator_name = x_iterator.__name__
    iterators_mapping[iterator_name] = x_iterator
    iterator_functions_mapping[iterator_name] = x_iterator_functions


def invocation_iterator(invocation_iterator_functions):
    # pull relevant pieces of specification into dictionary
    # (may have to create intermediate representation later)
    dikt = {}
    # dikt['info'] = spec_dict['info']
    # dikt['externalDocs'] = spec_dict['externalDocs']
    # might need to pass in parameters here too? unsure
    for f in invocation_iterator_functions:
        f(dikt)


def specification_iterator(specification_iterator_functions):
    dikt = {}
    for f in specification_iterator_functions:
        f(dikt)


def schemas_iterator(schemas_iterator_functions):
    dikt = {}

    for f in schemas_iterator_functions:
        f(dikt)


def paths_iterator(paths_iterator_functions):
    dikt = {}

    for f in paths_iterator_functions:
        f(dikt)
