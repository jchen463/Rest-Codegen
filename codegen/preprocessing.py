try:  # when just doing $ python3 main.py only below imports work
    import codegen.codegen_config as cfg
except ImportError as err:  # when packaged, only above imports work
    import codegen_config as cfg

def getEnumList(schema_obj):
    enumList = []

    for attribute_name, attribute in schema_obj['properties'].items():
        if 'enum' in attribute:
            enum = Enum(attribute_name, attribute['enum'])
            enumList.append(enum)
            
    return enumList

class Enum:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

def isRequired(attribute_name, requiredList):
    if requiredList is None:
        return False
    elif attribute_name in requiredList:
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

def models():
    
    models = []

    schemas = cfg.SPEC_DICT['components']['schemas']
    for schema_name, schema in schemas.items():
        model = Model(schema_name, schema)
        models.append(model)
        print(model.name)
        for i in model.properties:
            print(i.name)
            print(i.isRequired)
            print(i.type)
        for j in model.enums:
            print(j.name)
            print(j.attributes)

    cfg.TEMPLATE_VARIABLES['schemas'] = models


class Model:
    def __init__(self, name, schema_obj):
        self.name = name
        self.dependencies = None
        self.properties = getProperties(schema_obj)
        self.enums = getEnumList(schema_obj)
    
def getProperties(schema_obj):
    properties =  []
    for attribute_name, attribute_dikt in schema_obj['properties'].items():
        property = Property(attribute_name, attribute_dikt, schema_obj.get('required'))
        properties.append(property)
    
    return properties
            
class Property:
    def __init__(self, name, property_obj, requiredList):
        self.name = name
        self.type = getType(property_obj,0)
        self.isRequired = isRequired(name,requiredList)


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