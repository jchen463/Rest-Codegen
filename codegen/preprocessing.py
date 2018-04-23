try:  # when just doing $ python3 main.py only below imports work
    import codegen.codegen_config as cfg
except ImportError as err:  # when packaged, only above imports work
    import codegen_config as cfg


def init_template_context():
    models()
    cfg.TEMPLATE_CONTEXT['paths'] = get_paths_by_tag()


def get_paths_by_tag():
    paths_by_tag = {}
    methods = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace']
    for path_url, path_dict in cfg.SPEC_DICT['paths'].items():
        parent_dict = {
            'url': path_url,
            'summary': paths_dict.get('summary')
            'description': paths_dict.get('description')
            'servers': paths_dict.get('servers')
            'parameters': paths_dict.get('parameters')
        }
        for key, value in path_dict.items():
            if key.match(cfg.EXT_REGEX):
                parent_dict[key] = value
        for method in methods:
            operation_dict = path_dict.get(method)
            if operation_dict is not None:
                parent_dict['method'] = method
                add_to_paths(paths_by_tag, parent_dict, operation_dict)

    return paths_by_tag


def add_to_paths(paths_by_tag, parent_dict, operation_dict):
    path = Path(parent_dict, operation_dict)
    tag = path.tag
    if tag is None:
        tag = 'default'
    if tag not in paths_by_tag:
        paths_by_tag[tag] = [path]
    else:
        paths_by_tag[tag].append(path)


def models():

    models = []

    print(cfg.SPEC_DICT)

    schemas = cfg.SPEC_DICT['components']['schemas']

    for schema_name, schema in schemas.items():
        print("\n")
        print(schema)
        model = {
            'name': schema_name,
            'properties': {},  # key is property name, value is property type
            'dependencies': {},  # key is filename, value is class that is being imported
            'required': schema['required'],  # list
            'enums': {},  # Is this needed??
        }

        if 'required' in schema:
            model['required'] = schema['required']

        for attribute_name, attribute in schema['object'].properties.items():
            model['properties'][attribute_name] = attribute.__dict__
            # find the property, and insert dependencies into the model if needed
            attribute_type = getType(attribute, 0)
            # if attribute type is null or empty do not include it into the dictionary
            # resolve issues like if a user uses a class named datetime and datetime is not a class
            # in the language they're using, how do we know the difference of whether its type is ref
            # or if it's a library and should be imported ???
            if attribute_type != "" and attribute_type != 'null':
                model['properties'][attribute_name]['type'] = attribute_type

            enum = getattr(attribute, 'enum', None)
            if enum is not None:
                model['enums'][attribute_name] = enum

        models.append(model)

    # result
    print(models)
    cfg.TEMPLATE_CONTEXT['schemas'] = models


def getType(schema_obj, depth):
    ref = getattr(schema_obj, 'ref', None)
    if ref is not None:
        s = ref.split('/')[3]
        for x in range(depth):
            s += '>'
        return s

    if schema_obj.type == 'array':
        return 'Array<' + getType(schema_obj.items, depth + 1)

    # s = typeMapping[schema_obj.type]
    type_format = getattr(schema_obj, 'format', None)
    if type_format is not None:
        s = type_format
    else:
        s = schema_obj.type

    for x in range(depth):
        s += '>'
    return s
