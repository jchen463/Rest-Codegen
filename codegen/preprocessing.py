import TEMPLATE_VARIABLES from codegen_config.py

def models:
    
    models = []

    schema = spec.components.schemas

    for schema_name, schema in schemas.items():
        model = 
        {
            'name': schema['name'],
            'properties': {},  # key is property name, value is property type
            'dependencies': {},  # key is filename, value is class that is being imported
            'required': schema['object'].required, # list
            'enums': {},  # Is this needed??
        }
    
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

            enumList = getattr(attribute, 'enum', None)
            if enum is not None:
                model['enums'][attribute_name] = enumList

        models.append(model)

        # result
        TEMPLATE_VARIABLES['schemas'] = models
    
def getType(schema_obj, depth):
    ref = getattr(schema_obj, 'ref', None)
    if ref is not None:
        s = ref.split('/')[3]
        for x in range(depth):
            s += '>'
        return s

    if schema_obj.type == 'array':
        return 'Array<' + get_observable_type_string(schema_obj.items, depth + 1)
    
    # s = typeMapping[schema_obj.type]
    type_format = getattr(schema_obj, 'format', None)
    if type_format is not None:
        s = type_format
    else:
        s = schema_obj.type

    for x in range(depth):
        s += '>'
    return s
