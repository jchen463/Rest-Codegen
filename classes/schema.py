from .parse import parse_dict
from .parse import get_boolean
from .parse import get_object


class Schema:
    def __init__(self, dikt):
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

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects, mappings=mappings, booleans=booleans, arrays=arrays)

        for key, value in d.items():
            self.__setattr__(key, value)

        # additionalProperties can be boolean or object
        if 'additionalProperties' in dikt:
            self.additionalProperties = get_boolean(dikt['additionalProperties'])
            if self.additionalProperties is None:
                self.additionalProperties = get_object(
                    'additionalProperties', dikt['additionalProperties'])

        # these will be strings
        # any: default, example
        # array of any: enum

        # numbers: multipleOf, maximum, minimum, maxLength, minLength, maxProperties, minProperties are going to be strings
        # allOf, oneOf, anyOf, not may be a mapping rather than an array
        # items must be present if type is array
