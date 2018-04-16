try:  # when just doing $ python3 main.py only below imports work
    import codegen.codegen_config as cfg
except ImportError as err:  # when packaged, only above imports work
    import codegen_config as cfg

# def models():

#     models = []

#     print(cfg.SPEC_DICT)

#     schemas = cfg.SPEC_DICT['components']['schemas']

#     for schema_name, schema in schemas.items():
#         print("\n")
#         print(schema)
#         model = {
#             'name': schema_name,
#             'properties': {},  # key is property name, value is property type
#             'dependencies': {},  # key is filename, value is class that is being imported
#             'required': schema['required'], # list
#             'enums': {},  # Is this needed??
#         }

#         if 'required' in schema:
#             model['required'] = schema['required']
    
#         for attribute_name, attribute in schema['object'].properties.items():
#             model['properties'][attribute_name] = attribute.__dict__
#             # find the property, and insert dependencies into the model if needed
#             attribute_type = getType(attribute, 0)
#             # if attribute type is null or empty do not include it into the dictionary
#             # resolve issues like if a user uses a class named datetime and datetime is not a class
#             # in the language they're using, how do we know the difference of whether its type is ref
#             # or if it's a library and should be imported ??? 
#             if attribute_type != "" and attribute_type != 'null':
#                 model['properties'][attribute_name]['type'] = attribute_type

#             enum = getattr(attribute, 'enum', None)
#             if enum is not None:
#                 model['enums'][attribute_name] = enum

#         models.append(model)

#     # result
#     print(models)
#     cfg.TEMPLATE_VARIABLES['schemas'] = models
    
# def getType(schema_obj, depth):
#     ref = getattr(schema_obj, 'ref', None)
#     if ref is not None:
#         s = ref.split('/')[3]
#         for x in range(depth):
#             s += '>'
#         return s

#     if schema_obj.type == 'array':
#         return 'Array<' + getType(schema_obj.items, depth + 1)
    
#     # s = typeMapping[schema_obj.type]
#     type_format = getattr(schema_obj, 'format', None)
#     if type_format is not None:
#         s = type_format
#     else:
#         s = schema_obj.type

#     for x in range(depth):
#         s += '>'
#     return s

def getTypescriptType(attributes):
    ref = getattr(schema_obj, 'ref', None)
    if ref is not None:
        s = ref.split('/')[3]
        for x in range(depth):
            s += '>'
        return s

    if schema_obj.type == 'array':
        return 'Array<' + getTypescriptType(schema_obj.items, depth + 1)
    
    # s = typeMapping[schema_obj.type]
    type_format = getattr(schema_obj, 'format', None)
    if type_format is not None:
        s = type_format
    else:
        s = schema_obj.type

    for x in range(depth):
        s += '>'
    return s

    if attribute_type != "" and attribute_type != 'null':
        model['properties'][attribute_name]['type'] = attribute_type

def getEnumList(schema_obj):
    enumList = {}
    for attribute_name, attribute in schema_obj['properties'].items():
        if 'enum' in attribute:
            enumList.update({attribute_name:attribute['enum']})
                
    return enumList

def isRequired(schema_obj, attribute_name):
    if 'required' not in schema_obj:
        return False
    elif attribute_name in schema_obj['required']:
        return True
    else:
        return False 

def getType(schema_obj, depth):
    if '$ref' in schema_obj:
        ref = schema_obj['$ref']
        s = ref.split('/')[3]
        for x in range(depth):
            s += '>'
        return s

    if 'type' in schema_obj: 
        if type == 'array':
            return 'Array<' + get_observable_type_string(schema_obj.items, depth + 1)
        # s = typeMapping[schema_obj.type]
        type_format = getattr(schema_obj, 'format', None)
        if type_format is not None:
            s = type_format
        else:
            s = schema_obj['type']
    
    for x in range(depth):
        s += '>'

    return s

def getProperties(schema_obj):

    properties =  {}

    for attribute_name, attribute in schema_obj['properties'].items():
        properties.update({attribute_name: {}}) 
        properties[attribute_name].update({'type': getType(attribute,0) })
        properties[attribute_name].update({'isRequired': isRequired(schema_obj, attribute_name)})
    return properties

def models():
    
    models = []

    schemas = cfg.SPEC_DICT['components']['schemas']
    # print(schemas)
    for schema_name, schema in schemas.items():
        model = {
            'name': schema_name,
            'properties': getProperties(schema),
            'dependencies': {}, 
            'enums': getEnumList(schema)
        }
        print(model)
        models.append(model)
    
    cfg.TEMPLATE_VARIABLES['schemas'] = models