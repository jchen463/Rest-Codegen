import re

try:
    import codegen.codegen_config as cfg
except ImportError as err:
    import codegen_config as cfg


class Rep:
    def __repr__(self):
        return repr(vars(self))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__dict__ == other.__dict__


class Callback(Rep):
    def __init__(self, dikt):
        self.dikt = {}
        self.extensions = []
        for key, value in dikt.items():
            if ext_regex.match(key):
                self.extensions.append({key, value})
            else:
                self.dikt[key] = value


class Components(Rep):
    def __init__(self, dikt):
        allowed = ['schemas', 'responses', 'parameters',
                   'examples', 'requestBodies', 'headers',
                   'securitySchemes', 'links', 'callbacks',
                   'extensions']
        mappings = ['schemas', 'responses', 'parameters',
                    'examples', 'requestBodies', 'headers',
                    'securitySchemes', 'links', 'callbacks']
        self.__dict__ = parse_dict(
            dikt=dikt, allowed=allowed, mappings=mappings)


class Contact(Rep):
    def __init__(self, dikt):
        allowed = ['name', 'url', 'email', 'extensions']
        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed)


class Discriminator(Rep):
    def __init__(self, dikt):
        allowed = ['propertyName', 'mapping']
        required = ['propertyName']
        mappings = ['mapping']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                                   mappings=mappings)


class Encoding(Rep):
    def __init__(self, dikt):
        allowed = ['contentType', 'headers', 'style',
                   'explode', 'allowReserved', 'extensions']
        mappings = ['headers']
        booleans = ['explode', 'allowReserved']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed)


class Example(Rep):
    def __init__(self, dikt):
        allowed = ['summary', 'description', 'value',
                   'externalValue', 'extensions']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed)


class ExternalDocumentation(Rep):
    def __init__(self, dikt):
        allowed = ['description', 'url', 'extensions']
        required = ['url']

        self.__dict__ = parse_dict(
            dikt=dikt, allowed=allowed, required=required)


class Header(Rep):
    def __init__(self, dikt):
        if 'content' in dikt != 'schema' in dikt:
            raise ValueError("REQUIRED: one of 'content' or 'schema' only")
        if 'example' in dikt != 'examples' in dikt:
            raise ValueError(
                "REQUIRED: one of 'example' or 'examples' only")

        # All traits that are affected by the location MUST be applicable to a location of header (for ex. style)
        allowed = ['description',
                   'required', 'deprecated', 'allowEmptyValue',
                   'style', 'explode', 'allowReserved',
                   'schema', 'examples',
                   'content', 'extensions']
        required = []
        booleans = ['required', 'deprecated', 'allowEmptyValue'
                    'explode', 'allowReserved']
        mappings = ['content', 'examples']
        objects = ['schema']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                                   objects=objects, mappings=mappings, booleans=booleans, arrays=arrays)

        # <any>
        if 'example' in dikt:
            self.example = dikt['example']

        if dikt['in'] == 'path':
            required.append('required')

        # Default values
        # self.explode = False
        # if 'style' in dikt and dikt['style'] == 'form':
        # #     self.explode = True
        # self.required = False
        # self.allowReserved = False


class Info(Rep):
    def __init__(self, dikt):
        allowed = ['title', 'description', 'termsOfService',
                   'contact', 'license', 'version',
                   'extensions']
        required = ['title', 'version']
        objects = ['contact', 'license']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed,
                                   required=required, objects=objects)


class License(Rep):
    def __init__(self, dikt):

        allowed = ['name', 'url', 'extensions']
        required = ['name']

        self.__dict__ = parse_dict(
            dikt=dikt, allowed=allowed, required=required)


class Link(Rep):
    def __init__(self, dikt):
        allowed = ['operationRef', 'operationId',
                   'requestBody', 'description', 'server',
                   'extensions']
        objects = ['server']

        # parameters and requestBody can be <any | {expression}>
        self.parameters = None
        if 'parameters' in dikt:
            self.parameters = get_mapping('scopes', dikt['parameters'])

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, objects=objects,
                                   mappings=mappings)


class MediaType(Rep):
    def __init__(self, dikt):
        allowed = ['schema', 'example', 'examples',
                   'encoding', 'extensions']
        objects = ['schema']
        mappings = ['examples', 'encoding']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, objects=objects,
                                   mappings=mappings)


class OAuthFlow(Rep):
    def __init__(self, dikt, flow_name):
        allowed = ['authorizationCode', 'tokenUrl',
                   'refreshUrl', 'scopes', 'extensions']
        required = ['scopes']
        mappings = ['scopes']

        flows_requiring_tokenUrl = ['password',
                                    'clientCredentials', 'authorizationCode']
        flows_requiring_authorizationUrl = ['implicit', 'authorizationCode']
        if flow_name in flows_requiring_tokenUrl:
            required.append('tokenUrl')
        if flow_name in flows_requiring_authorizationUrl:
            required.append('authorizationUrl')

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed,
                                   required=required, mappings=mappings)


class OAuthFlows(Rep):
    def __init__(self, dikt):
        allowed = ['extensions']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed)

        self.implicit = None
        self.password = None
        self.clientCredentials = None
        self.authorizationCode = None

        if 'implicit' in dikt:
            self.implicit = OAuthFlow(dikt['implicit'], 'implicit')
        if 'password' in dikt:
            self.password = OAuthFlow(dikt['password'], 'password')
        if 'clientCredentials' in dikt:
            self.clientCredentials = OAuthFlow(
                dikt['clientCredentials'], 'clientCredentials')
        if 'authorizationCode' in dikt:
            self.authorizationCode = OAuthFlow(
                dikt['authorizationCode'], 'authorizationCode')


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
        self.__dict__ = parse_dict(
            dikt=dikt, allowed=allowed, required=required)


class RequestBody(Rep):
    def __init__(self, dikt):
        allowed = ['description', 'content', 'required',
                   'extensions']
        required = ['content']
        mappings = ['content']
        booleans = ['required']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                                   mappings=mappings, booleans=booleans)


class Response(Rep):
    def __init__(self, dikt):
        allowed = ['description', 'headers', 'content',
                   'links', 'extensions']
        required = ['description']
        mappings = ['headers', 'content', 'links']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                                   mappings=mappings)


class Schema(Rep):
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
        allowed = ['url', 'description', 'variables', 'extensions']
        required = ['url']
        mappings = ['variables']

        self.__dict__ = parse_dict(
            dikt=dikt, allowed=allowed, required=required, mappings=mappings)


class ServerVariable(Rep):
    def __init__(self, dikt):
        allowed = ['enum', 'default', 'description', 'extensions']
        required = ['default']
        arrays = ['enum']

        self.__dict__ = parse_dict(
            dikt=dikt, allowed=allowed, required=required, arrays=arrays)


class Specification(Rep):
    def __init__(self, dikt):
        allowed = ['openapi', 'info', 'servers', 'paths',
                   'components', 'security', 'tags', 'externalDocs']
        required = ['openapi', 'info', 'paths']
        objects = ['info', 'paths', 'components', 'externalDocs']
        arrays = ['servers', 'security', 'tags']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed,
                                   required=required, objects=objects, arrays=arrays)


class Tag(Rep):
    def __init__(self, dikt):
        allowed = ['name', 'description', 'externalDocs', 'extensions']
        required = ['name']
        objects = ['externalDocs']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                                   objects=objects)


class XML(Rep):
    def __init__(self, dikt):
        allowed = ['name', 'namespace', 'prefix',
                   'attribute', 'wrapped', 'extensions']
        required = ['name']
        booleans = ['attribute', 'wrapped']

        self.__dict__ = parse_dict(dikt=dikt, allowed=allowed, required=required,
                                   booleans=booleans)


"""
PARSING FUNCTIONS
"""


def parse_dict(dikt, allowed, required=[], objects=[], mappings=[], booleans=[], arrays=[]):
    d = {}
    for attr in required:
        if attr not in dikt:
            raise ValueError('required field ' + attr + ' is missing')
    for attr in allowed:
        d[attr] = None

    d['extensions'] = []

    for key, value in dikt.items():
        if key in objects:
            d[key] = get_object(key, value)
        elif key in mappings:
            d[key] = get_mapping(key, value)
        elif key in arrays:
            d[key] = get_array(key, value)
        elif key in booleans:
            d[key] = get_boolean(value)
        elif ext_regex.match(key):
            d['extensions'].append({key: value})
        else:  # string
            d[key] = value

    for key, value in list(d.items()):
        if key not in allowed:
            del d[key]

    return d


def get_mapping(keyword, dikt):
    mapping = {}

    for key, value in dikt.items():
        mapping[key] = get_object(keyword, value)

    return mapping


def get_array(keyword, arr):
    array = []

    for dikt in arr:
        array.append(get_object(keyword, dikt))

    return array


def get_boolean(value):
    if type(value) == bool:
        return value
    if type(value) == str and value.lower() == 'true':
        return True
    if type(value) == str and value.lower() == 'false':
        return False
    return None


def get_object(keyword, dikt):
    if '$ref' in dikt:
        return Reference(dikt)
        # ref = dikt['$ref'][2:].split('/')
        # return get_object(ref[1], cfg.SPEC_DICT[ref[0]][ref[1]][ref[2]])
    if keyword in keyword_to_object:
        return keyword_to_object[keyword](dikt)
    return None


def return_arg(arg):
    return arg


ext_regex = re.compile('x-.*')

keyword_to_object = {
    # mapping keywords
    'variables': ServerVariable,
    'schemas': Schema,
    'callbacks': Callback,
    'mapping': return_arg,
    'responses': Response,
    'headers': Header,
    'content': MediaType,
    'examples': Example,
    'encoding': Encoding,
    'links': Link,
    'parameters': Parameter,
    'requestBodies': RequestBody,
    'securitySchemes': SecurityScheme,
    'scopes': return_arg,
    'properties': Schema,

    # object keywords
    'info': Info,
    'contact': Contact,
    'license': License,
    'paths': Paths,
    'get': Operation,
    'put': Operation,
    'post': Operation,
    'delete': Operation,
    'options': Operation,
    'head': Operation,
    'patch': Operation,
    'trace': Operation,
    'externalDocs': ExternalDocumentation,
    'requestBody': RequestBody,
    'components': Components,
    'discriminator': Discriminator,
    'xml': XML,
    'schema': Schema,
    'flows': OAuthFlows,
    'items': Schema,
    'additionalProperties': Schema,
    '/': PathItem,

    # array keywords
    'servers': Server,
    'security': SecurityRequirement,
    'tags': Tag,
    'parameters': Parameter,
    'op_tags': return_arg,  # Operation Object tags
    'allOf': Schema,
    'oneOf': Schema,
    'anyOf': Schema,
    'not': Schema,
    'required': return_arg,
    'enum': return_arg,
}
