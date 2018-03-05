import re


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
        from .reference import Reference
        return Reference(dikt)
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
