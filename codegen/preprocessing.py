try:  # when just doing $ python3 main.py only below imports work
    import codegen.codegen_config as cfg
except ImportError as err:  # when packaged, only above imports work
    import codegen_config as cfg


def init_template_context():
    models()
    cfg.TEMPLATE_CONTEXT['paths'] = get_paths_by_tag()

def get_paths_by_tag():
    paths = {}

    for path_url, path_object in cfg.SPEC_OBJ.paths.dikt.items():
        collect_paths(paths, path_object.get, path_url, 'get')
        collect_paths(paths, path_object.put, path_url, 'put')
        collect_paths(paths, path_object.post, path_url, 'post')
        collect_paths(paths, path_object.delete, path_url, 'delete')
        collect_paths(paths, path_object.options, path_url, 'options')
        collect_paths(paths, path_object.head, path_url, 'head')
        collect_paths(paths, path_object.patch, path_url, 'patch')
        collect_paths(paths, path_object.trace, path_url, 'trace')

    return paths


def collect_paths(paths_dict, operation_object, path_url, method):
    if operation_object is not None:
        tags = operation_object.tags
        if tags != []:
            if tags[0] not in paths_dict:
                paths_dict[tags[0]] = []
            paths_dict[tags[0]].append(get_path_dict(path_url, method, tags, operation_object))
        else:
            if 'default' not in paths_dict:
                paths_dict['default'] = []
            paths_dict['default'].append(get_path_dict(path_url, method, ['default'], operation_object))


def get_path_dict(path_url, method, tags, properties):
    return {
        'url': path_url,
        'method': method,
        'tag': tags[0],
        'operationId': properties.operationId,
        'parameters': get_parameters(),
        'requestBody': get_request_body(),
        'responses': get_responses(),
        'callbacks': properties.callbacks,
        'security': properties.security,
        'servers': properties.servers,
    }


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
