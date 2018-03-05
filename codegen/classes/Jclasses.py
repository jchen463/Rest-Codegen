class Rep:
    def __repr__(self):
        return repr(vars(self))

class Operation(Rep):
    def __init__(self, dikt):
        allowed = ['summary', 'description', 'externalDocs',
                   'operationId', 'parameters', 'requestBody',
                   'responses', 'callbacks', 'deprecated',
                   'security', 'servers', 'extensions']
        required = ['responses']
        objects = ['externalDocs', 'requestBody']
        mappings = ['callbacks']
        arrays = ['parameters', 'security', 'servers']
        booleans = ['deprecated']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects, mappings=mappings, booleans=booleans,
                       arrays=arrays)

        if 'tags' in dikt:
            self.tags = parse.get_array('op_tags', dikt['tags'])
        else:
            self.tags = None

        self.responses = {}
        for key, value in dikt['responses']:
            self.responses[key] = parse.get_object('responses', value)

class Parameter(Rep):
    def __init__(self, dikt):

        if 'content' in dikt != 'schema' in dikt:
            raise ValueError('REQUIRED: one of \'content\' or \'schema\' only')
        if 'example' in dikt != 'examples' in dikt:
            raise ValueError(
                'REQUIRED: one of \'example\' or \'examples\' only')

        allowed = ['name', 'in', 'description',
                   'required', 'deprecated', 'allowEmptyValue',
                   'style', 'explode', 'allowReserved',
                   'schema', 'examples',
                   'content', 'extensions']
        required = ['name', 'in']
        booleans = ['required', 'deprecated', 'allowEmptyValue'
                                              'explode', 'allowReserved']
        mappings = ['content', 'examples']
        objects = ['schema']

        if dikt['in'] == 'path':
            required.append('required')

        # Default values
        # self.explode = False
        # if 'style' in dikt and dikt['style'] == 'form':
        # #     self.explode = True
        # self.required = False
        # self.allowReserved = False

        # <any>

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects, mappings=mappings, booleans=booleans)

        if 'example' in dikt:
            self.example = dikt['example']

    """
    Rules for serialization of parameter:
    For simple scenarios, a 'schema' and 'style' can describe the structure and syntax of the parameter
    For complex scenarios, the content property can define the media type and schema of the parameter
    A parameter MUST contain either a schema property or a content property, but not both.
    When example or examples is provided along with the schema object, the example MUST follow the prescribed serialization strategy for the parameter
    """


class PathItem(Rep):
    def __init__(self, dikt):
        allowed = ['summary', 'description',
                   'get', 'put', 'post',
                   'delete', 'options', 'head',
                   'patch', 'trace', 'servers',
                   'parameters', 'extensions']
        objects = ['get', 'put', 'post',
                   'delete', 'options', 'head',
                   'patch', 'trace']
        arrays = ['servers', 'parameters']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed)

        self.ref = None
        if '$ref' in dikt:
            self.ref = dikt['$ref']

class Paths(Rep):
    def __init__(self, dikt):

        self.dikt = {}
        self.extensions = []
        for key, value in dikt.items():
            if ext_regex.match(key):
                self.extensions.append({key: value})
            else:
                self.dikt[key] = get_object('/', value)

class Reference(Rep):
    def __init__(self, dikt):
        allowed = ['$ref']
        required = ['$ref']
        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required)


class RequestBody(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['description', 'content', 'required',
                   'extensions']
        required = ['content']
        mappings = ['content']
        booleans = ['required']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       mappings=mappings, booleans=booleans)


class Response(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['description', 'headers', 'content',
                   'links', 'extensions']
        required = ['description']
        mappings = ['headers', 'content', 'links']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       mappings=mappings)


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

        self.__dict__ = d

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

        # these will be strings
        # any: default, example
        # array of any: enum

        # numbers: multipleOf, maximum, minimum, maxLength, minLength, maxProperties, minProperties are going to be strings
        # allOf, oneOf, anyOf, not is type: [<Schema Object | Reference Object>]
        # items must be present if type is array


class SecurityRequirement(Rep):
    def __init__(self, dikt):
        for key, value in dikt.items():
            self.name = key
            self.array = value


class SecurityScheme(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['type', 'description', 'name',
                   'in', 'scheme', 'bearerFormat',
                   'flows', 'openIdConnectUrl', 'extensions']
        required = ['type']
        objects = ['flows']

        allowed_types = ['apiKey', 'http', 'oauth2', 'openIdConnect']

        if 'type' not in dikt or dikt['type'] not in allowed_types:
            raise ValueError(
                'type field must be one of: apiKey, http, oauth2, openIdConnect')

        if dikt['type'] == 'apiKey':
            required.append('name')
            required.append('in')
        if dikt['type'] == 'http':
            required.append('scheme')
        if dikt['type'] == 'oauth2':
            required.append('flows')
        if dikt['type'] == 'openIdConnect':
            required.append('openIdConnectUrl')

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, objects=objects)


class Server(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['url', 'description', 'variables', 'extensions']
        required = ['url']
        mappings = ['variables']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required, mappings=mappings)


class ServerVariable(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['enum', 'default', 'description', 'extensions']
        required = ['default']
        arrays = ['enum']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required, arrays=arrays)


class Specification(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['openapi', 'info', 'servers', 'paths',
                   'components', 'security', 'tags', 'externalDocs']
        required = ['openapi', 'info', 'paths']
        objects = ['info', 'paths', 'components', 'externalDocs']
        arrays = ['servers', 'security', 'tags']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, objects=objects, arrays=arrays)

class Tag(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['name', 'description', 'externalDocs', 'extensions']
        required = ['name']
        objects = ['externalDocs']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects)


class XML(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['name', 'namespace', 'prefix',
                   'attribute', 'wrapped', 'extensions']
        required = ['name']
        booleans = ['attribute', 'wrapped']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       booleans=booleans)
