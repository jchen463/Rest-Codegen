try:  # when just doing $ python3 main.py only below imports work
    import codegen.codegen_config as cfg
except ImportError as err:  # when packaged, only above imports work
    import codegen_config as cfg

#write print functions!!!

class Model:
    def __init__(self, name):
        self.name = name
        self.dependencies = {}
        self.properties = {}
        self.required = {}
        self.enums = {}
        # self.properties = getProperties(schema_obj)
        # self.enums = getEnumList(schema_obj)

class Property:
    def __init__(self, name):
        self.name = name
        self.type = None
        self.isRequired = None
        # self.type = getType(property_obj,0)
        # self.isRequired = isRequired(name,requiredList)

class Enum:
    def __init__(self, values):
        #self.name = name
        self.values = values

def models():

    #initialize array to hold model and scheamas for use below
    models = {}
    schemas = cfg.SPEC_DICT['components']['schemas']

    #iterate through each schema
    for schema_name, schema in schemas.items():

        #create a model dictionary for each schema
        #model = {
        #    'name': schema_name,
        #    'properties': {},  # key is property name, value is property type
        #    'dependencies': {},  # key is filename, value is class that is being imported. **NOT SURE IF THIS WILL BE KEPT**
        #    'required': [], # list of the required variables in each schema
        #    'enums': {},  # Is this needed??
        #}
        model = Model(schema_name)



        # get the required list of items
        #if 'required' in schema:
        #    model['required'] = schema['required']
        model.required = schema.get('required')


        for attribute_name, attribute in schema['properties'].items():

            #model['properties'][attribute_name] = {}
            model.properties[attribute_name] = Property(attribute_name)

            # find the property, and insert dependencies into the model if needed
            attribute_type = getType(attribute, 0)

            if attribute_type != "" and attribute_type != 'null':
                #print(model)
                #print(attribute_name)
                #print(attribute_type)
                #model['properties'][attribute_name]['type'] = attribute_type
                model.properties[attribute_name].type = attribute_type

            #if 'enum' in attribute:
            #    model['enums'][attribute_name] = attribute['enum']

            if 'enum' in attribute:
                model.enums[attribute_name] = Enum(attribute.get('enum'))

        models[model.name] = model

    # result
    for model1 in models:
        print(model1)
    cfg.TEMPLATE_VARIABLES['schemas'] = models

def getType(schema_obj, depth):

    if '$ref' in schema_obj:
        s = schema_obj['$ref'].split('/')[3]
        for x in range(depth):
            s += '>'
        return s

    if schema_obj['type'] == 'array':
        return 'Array<' + getType(schema_obj['items'], depth + 1)

    # s = typeMapping[schema_obj.type]
    type_format = getattr(schema_obj, 'format', None)
    if type_format is not None:
        s = type_format
    else:
        s = schema_obj['type']

    for x in range(depth):
        s += '>'
    return s

def getEnumList(schema_obj):
    enumList = {}
    for attribute_name, attribute in schema_obj['properties'].items():
        if 'enum' in attribute:
            enumList.update({attribute_name: attribute['enum']})

    return enumList


def getRequiredList(schema_obj, attribute_name):
    if 'required' not in schema_obj:
        return False
    elif attribute_name in schema_obj['required']:
        return True
    else:
        return False

def getProperties(schema_obj):
    properties = {}

    for attribute_name, attribute in schema_obj['properties'].items():
        properties.update({attribute_name: {}})
        properties[attribute_name].update({'type': getType(attribute, 0)})
        properties[attribute_name].update({'isRequired': isRequired(schema_obj, attribute_name)})
    return properties