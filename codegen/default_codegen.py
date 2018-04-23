import os

import jinja2
import collections  # for OrderedDict

try:  # when just doing $ python3 main.py only below imports work
    import codegen.codegen_config as cfg
except ImportError as err:  # when packaged, only above imports work
    import codegen_config as cfg

iterators_mapping = collections.OrderedDict()
iterator_functions_mapping = collections.OrderedDict()


def codegen_stage(x_iterator, x_iterator_functions):
    iterator_name = x_iterator.__name__
    iterators_mapping[iterator_name] = x_iterator
    iterator_functions_mapping[iterator_name] = x_iterator_functions


def emit_template(template_path, params, output_dir, output_name):
    try:
        # check for their custom templates
        template_name = template_path.split('/')[-1]
        template_loader = jinja2.FileSystemLoader(os.getcwd() + os.path.sep + cfg.TEMPLATES_DIR)
        env = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True, line_comment_prefix='//*')
        template = env.get_template(template_name)  # template_path is something like: flask_server/model.j2, so we have to do a name comparison here
        print("outputed file \" " + output_name + " \" from user defined template")
    except jinja2.exceptions.TemplateNotFound as err:
        # check for template in our package
        try:
            template_loader = jinja2.PackageLoader('codegen', 'templates')
            env = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True, line_comment_prefix='//*')
            template = env.get_template(template_path)
        except jinja2.exceptions.TemplateNotFound as err:
            raise ValueError('template does not exist')

    env.globals['cfg'] = cfg
    output_file = output_dir + os.path.sep + output_name

    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(output_file, 'w') as outfile:
        outfile.write(template.render(params))


def run_iterators():
    # run each iterator once
    for iterator_name, iterator in iterators_mapping.items():
        iterator(cfg.TEMPLATE_VARIABLES , iterator_functions_mapping[iterator_name])


def invocation_iterator(spec, invocation_iterator_functions):
    #dikt = {}
    #dikt['info'] = spec.info
    #dikt['externalDocs'] = spec.externalDocs
    for f in invocation_iterator_functions:
        f()


def specification_iterator(spec, specification_iterator_functions):
    #paths_by_tag = get_paths_by_tag(spec.paths.dikt)
    #schemas = spec.components.schemas  # array of schemas
    #dikt = {'tags': paths_by_tag.keys(), 'models': schemas.keys()}

    for f in specification_iterator_functions:
        f()


def schemas_iterator(spec, schemas_iterator_functions):

    for schema_name, schema in cfg.TEMPLATE_VARIABLES['schemas'].items():
        spec['_current_schema'] = schema_name
        print(schema_name)
        print(schema)
        print("\n")
        for f in schemas_iterator_functions:
            f()


def paths_iterator(spec, paths_iterator_functions):
    pass

