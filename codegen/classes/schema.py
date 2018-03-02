from .rep import Rep


class Schema(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict
        from .parse import get_boolean
        from .parse import get_object

        allowed = ['title', 'multipleOf', 'maximum',
                   'exclusiveMaximum', 'minimum', 'exclusiveMinimum',
                   'maxLength', 'minLength', 'pattern',
                   'maxItems', 'minItems', 'uniqueItems',
                   'maxProperties', 'minProperties', 'required',
                   'type', 'allOf', 'default',
                   'oneOf', 'anyOf', 'not',
                   'items', 'properties', 'example',
                   'description', 'format', 'enum',
                   'nullable', 'discriminator', 'readOnly',
                   'writeOnly', 'xml', 'externalDocs', 'deprecated', 'extensions']
        required = []
        mappings = ['properties']
        objects = ['items', 'xml', 'externalDocs', 'discriminator']
        arrays = ['allOf', 'oneOf', 'anyOf', 'not', 'required', 'enum']
        booleans = ['nullable', 'readOnly,', 'writeOnly', 'deprecated',
                    'exclusiveMaximum', 'exclusiveMinimum', 'uniqueItems', ]

        if 'type' in dikt and dikt['type'] == 'array':
            required.append('items')

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects, mappings=mappings, booleans=booleans, arrays=arrays)

        self.title = d['title']
        self.exclusiveMaximum = d['exclusiveMaximum']
        self.exclusiveMinimum = d['exclusiveMinimum']
        self.pattern = d['pattern']
        self.uniqueItems = d['uniqueItems']
        self.required = d['required']
        self.type = d['type']
        self.allOf = d['allOf']
        self.default = d['default']
        self.oneOf = d['oneOf']
        self.anyOf = d['anyOf']
        self.notOf = d['not']
        self.items = d['items']
        self.properties = d['properties']
        self.example = d['example']
        self.description = d['description']
        self.format = d['format']
        self.enum = d['enum']
        self.nullable = d['nullable']
        self.discriminator = d['discriminator']
        self.readOnly = d['readOnly']
        self.writeOnly = d['writeOnly']
        self.xml = d['xml']
        self.externalDocs = d['externalDocs']
        self.deprecated = d['deprecated']
        self.extensions = d['extensions']

        # additionalProperties can be boolean or object if it exists
        self.additionalProperties = None
        if 'additionalProperties' in dikt:
            self.additionalProperties = get_boolean(
                dikt['additionalProperties'])
            if self.additionalProperties is None:  # if it wasn't a boolean
                self.additionalProperties = get_object(
                    'additionalProperties', dikt['additionalProperties'])

        # these fields should be numbers or None
        if d['multipleOf'] is not None:
            self.multipleOf = int(d['multipleOf'])
        if d['maximum'] is not None:
            self.maximum = int(d['maximum'])
        if d['minimum'] is not None:
            self.minimum = int(d['minimum'])
        if d['maxItems'] is not None:
            self.maxItems = int(d['maxItems'])
        if d['minItems'] is not None:
            self.minItems = int(d['minItems'])
        if d['maxProperties'] is not None:
            self.maxProperties = int(d['maxProperties'])
        if d['minProperties'] is not None:
            self.minProperties = int(d['minProperties'])
        if d['minLength'] is not None:
            self.minLength = int(d['minLength'])
        if d['maxLength'] is not None:
            self.maxLength = int(d['maxLength'])
            
    def __eq__(self, other):
        return self.title == other.title and self.exclusiveMaximum == other.exclusiveMaximum \
           and self.exclusiveMinimum == other.exclusiveMinimum and self.pattern == other.pattern \
           and self.uniqueItems == other.uniqueItems and self.required == other.required \
           and self.type == other.type and self.allOf == other.allOf \
           and self.default == other.default and self.oneOf == other.oneOf \
           and self.anyOf == other.anyOf and self.notOf == other.notOf \
           and self.items == other.items and self.properties == other.properties \
           and self.example == other.example and self.description == other.description \
           and self.format == other.format and self.enum == other.enum \
           and self.nullable == other.nullable and self.discriminator == other.discriminator \
           and self.readOnly == other.readOnly and self.writeOnly == other.writeOnly \
           and self.xml == other.xml and self.externalDocs == other.externalDocs \
           and self.deprecated == other.deprecated and self.extensions == other.extensions \
           and self.additionalProperties == other.additionalProperties and self.multipleOf == other.multipleOf \
           and self.maximum == other.maximum and self.minimum == other.minimum \
           and self.maxItems == other.maxItems and self.minItems == other.minItems \
           and self.maxProperties == other.maxProperties and self.minProperties == other.minProperties \
           and self.minLength == other.minLength and self.maxLength == other.maxLength
 
    def __ne__(self, other):
        return self.title != other.title and self.exclusiveMaximum != other.exclusiveMaximum \
           and self.exclusiveMinimum != other.exclusiveMinimum and self.pattern != other.pattern \
           and self.uniqueItems != other.uniqueItems and self.required != other.required \
           and self.type != other.type and self.allOf != other.allOf \
           and self.default != other.default and self.oneOf != other.oneOf \
           and self.anyOf != other.anyOf and self.notOf != other.notOf \
           and self.items != other.items and self.properties != other.properties \
           and self.example != other.example and self.description != other.description \
           and self.format != other.format and self.enum != other.enum \
           and self.nullable != other.nullable and self.discriminator != other.discriminator \
           and self.readOnly != other.readOnly and self.writeOnly != other.writeOnly \
           and self.xml != other.xml and self.externalDocs != other.externalDocs \
           and self.deprecated != other.deprecated and self.extensions != other.extensions \
           and self.additionalProperties != other.additionalProperties and self.multipleOf != other.multipleOf \
           and self.maximum != other.maximum and self.minimum != other.minimum \
           and self.maxItems != other.maxItems and self.minItems != other.minItems \
           and self.maxProperties != other.maxProperties and self.minProperties != other.minProperties \
           and self.minLength != other.minLength and self.maxLength != other.maxLength

        # these will be strings
        # any: default, example
        # array of any: enum

        # numbers: multipleOf, maximum, minimum, maxLength, minLength, maxProperties, minProperties are going to be strings
        # allOf, oneOf, anyOf, not is type: [<Schema Object | Reference Object>]
        # items must be present if type is array
