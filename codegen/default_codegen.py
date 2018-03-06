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


def run_iterators():
    # run each iterator once
    for iterator_name, iterator in iterators_mapping.items():
        iterator(cfg.SPECIFICATION, iterator_functions_mapping[iterator_name])


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
    schemas = spec.components.schemas  # array of schemas
    for schema_name, schema in schemas.items():
        for f in schemas_iterator_functions:
            f({'name': schema_name, 'object': schema})

def paths_iterator(spec, paths_iterator_functions):
    paths_by_tag = get_paths_by_tag(spec.paths.dikt)
    basePath = {'basePath': spec.servers[0].url }
    """
    paths_by_tag = {
        'pet': [
            {
                'url': ,
                'method': ,
                'tags': ,
                'info': ,
            },
            {

            },
        ],
        'user': [
            {

            },
            {

            },
        ]
    }
    """

    tags = {'tags': paths_by_tag.keys()}
    #emit_template('main.tmpl', tags, cfg.PROJECT_OUTPUT, '__main__.py')
    for tag, path_dicts in paths_by_tag.items():
        for f in paths_iterator_functions:
            path_dicts[0].update(basePath)
           # print(path_dicts)
            f(path_dicts)


def get_paths_by_tag(paths_dict):
    paths = {}

    for path_url, path_object in paths_dict.items():
        collect_paths(paths, path_object.get, path_url, 'get')
        collect_paths(paths, path_object.put, path_url, 'put')
        collect_paths(paths, path_object.post, path_url, 'post')
        collect_paths(paths, path_object.delete, path_url, 'delete')
        collect_paths(paths, path_object.options, path_url, 'options')
        collect_paths(paths, path_object.head, path_url, 'head')
        collect_paths(paths, path_object.patch, path_url, 'patch')
        collect_paths(paths, path_object.trace, path_url, 'trace')

    return paths


def collect_paths(paths, operation_object, path_url, method):
    if operation_object is not None:
        tags = operation_object.tags
        if tags != []:
            if tags[0] not in paths:
                paths[tags[0]] = []
            paths[tags[0]].append(get_path_dict(path_url, method, tags, operation_object))
        else:
            if 'default' not in paths:
                paths['default'] = []
            paths['default'].append(get_path_dict(path_url, method, tags, operation_object))


def get_path_dict(path_url, method, tags, info):
    return {
        'url': path_url,
        'method': method,
        'tag': tags[0],
        'properties': info, # Operation Object
    }
