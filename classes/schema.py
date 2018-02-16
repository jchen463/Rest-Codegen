from .parse import parse_dict


class Schema:
    def __init__(self, dikt):
        allowed = ['title', 'multipleOf', 'maximum',
                   'exclusiveMaximum', 'minimum', 'exclusiveMinimum',
                   'maxLength', 'minLength', 'pattern',
                   'maxItems', 'minItems', 'uniqueItems',
                   'maxProperties', 'minProperties', 'required',
                   'enum', 'type', 'allOf',
                   'oneOf', 'anyOf', 'not',
                   'items', 'properties', 'additionalProperties',
                   'description', 'format',
                   'nullable', 'discriminator', 'readOnly',
                   'writeOnly', 'xml', 'externalDocs', 'deprecated', 'extensions']
        required = []
        mappings = ['properties']
        objects = ['items', 'xml', 'externalDocs', 'discriminator']
        arrays = ['allOf', 'oneOf', 'anyOf', 'not', 'enum', 'required']
        booleans = ['nullable', 'readOnly,', 'writeOnly', 'deprecated',
                    'exclusiveMaximum', 'exclusiveMinimum', 'uniqueItems', ]

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects, mappings=mappings, booleans=booleans, arrays=arrays)
        # any: default, example
        # additionalProperties can be boolean or object
        # numbers: multipleOf, maximum, minimum, maxLength, minLength
        # allOf, oneOf, anyOf, not may be a mapping rather than an array
        # items must be present if type is array
