import os

import jinja2


try:  # when just doing $ python3 main.py only below imports work
    import codegen.codegen_config as cfg
except ImportError as err:  # when packaged, only above imports work
    import codegen_config as cfg

iterators_mapping = {}
iterator_functions_mapping = {}


def codegen_stage(x_iterator, x_iterator_functions):
    iterator_name = x_iterator.__name__
    iterators_mapping[iterator_name] = x_iterator
    iterator_functions_mapping[iterator_name] = x_iterator_functions


def invocation_iterator(spec, invocation_iterator_functions):
    # pull relevant pieces of specification into dictionary
    # (may have to create intermediate representation later)
    # might need to pass in parameters here too? unsure
    # also unsure what object we're going to pass into these functions
    # dikt = {}
    # dikt['info'] = spec_dict['info']
    # dikt['externalDocs'] = spec_dict['externalDocs']
    for f in invocation_iterator_functions:
        f(spec)


def specification_iterator(spec, specification_iterator_functions):
    # right now we're only using one spec though
    # for specification in specifications:
    #     for f in specification_iterator_functions:
    #         f(specification)
    for f in specification_iterator_functions:
        f(spec)


def schemas_iterator(spec, schemas_iterator_functions):
    # schemas = spec.components['schemas']  # array of schemas
    # for schema in schemas:
    #     for f in schemas_iterator_functions:
    #         f(schema)
    for f in schemas_iterator_functions:
        f(spec)


def paths_iterator(spec, paths_iterator_functions):
    paths = spec.paths.dikt  # dictionary where pathname is key and path details is value
    # create a dictionary where tag is key and all following paths is value
    # probably need to change this to an array of path objects -- may need to refactor Paths class
    # for path_grouping in paths:
    #     for f in paths_iterator_functions:
    #         f(dikt)
    for f in paths_iterator_functions:
        f(spec)

# paths are stored as a dictionary
# group paths by tag
# execute each function once per path-group

# paths = {
#     'pet': [
#         Path object,
#         Path object,
#         Path object,
#     ],
#     'user': [
#         Path object,
#         Path object,
#     ],
#     'store': [

#     ]
# }


def run_iterators():
    # run each iterator once
    for iterator_name, iterator in iterators_mapping.items():
        iterator(cfg.SPECIFICATION, iterator_functions_mapping[iterator_name])


def emit_template(template_name, params, output_dir, output_name):
    # template_loader = jinja2.FileSystemLoader(searchpath='./')

    # THIS DOESN'T WORK WHEN RUNNING 'python3 main.py'
    # we have to use FileSystemLoader for ^^^
    # jinja2 will load templates from our package's 'templates/' folder
    template_loader = jinja2.PackageLoader('codegen', 'templates')
    # jinja2 will look for templates in the templates folder in the installed codegen package
    env = jinja2.Environment(loader=template_loader,
                             trim_blocks=True,
                             lstrip_blocks=True,
                             line_comment_prefix='//*')

    # template_path = cfg.DEFAULT_TEMPLATES_DIR + os.path.sep + template_name
    output = env.get_template(template_name).render(params)

    output_file = output_dir + os.path.sep + output_name

    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(output_file, 'w') as outfile:
        outfile.write(output)
