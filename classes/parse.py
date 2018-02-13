import re

ext_regex = re.compile('x-.*')


def parse_dict(dikt, allowed, required=[], objects=[], mappings=[], booleans=[], arrays=[], anys=[]):
    d = {}
    # for attr in required:
    #     if attr not in dikt:
    #         raise ValueError('required field ' + attr + ' is missing')
    for attr in allowed:
        d[attr] = None

    d['extensions'] = []

    for key, value in dikt.items():
        if key in objects:
            d[key] = get_object(key, value)
        elif key in mappings:
            d[key] = get_mapping(key, value)
        elif key in arrays:  # server: [<Server Object>]
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

    if keyword_to_type[keyword] == 'string':
        for key, value in dikt.items():
            mapping[key] = value
    else:  # Object or ref string
        for key, value in dikt.items():
            mapping[key] = get_object(keyword, value)

    return mapping


def get_array(keyword, arr):
    array = []  # list

    for dikt in arr:
        array.append(get_object(keyword, dikt))

    return array


def get_boolean(value):
    if type(value) == bool:
        return value
    if type(value) == str and value.lower() == 'true':
        return True
    return False


def get_object(keyword, dikt):
    if keyword_to_type[keyword] == 'Info':
        from .info import Info
        return Info(dikt)
    if keyword_to_type[keyword] == 'Contact':
        from .contact import Contact
        return Contact(dikt)
    if keyword_to_type[keyword] == 'License':
        from .license_spec import License
        return License(dikt)
    if keyword_to_type[keyword] == 'Server':
        from .server import Server
        return Server(dikt)
    if keyword_to_type[keyword] == 'ServerVariable':
        from .server_variable import ServerVariable
        return ServerVariable(dikt)
    if keyword_to_type[keyword] == 'Paths':
        from .paths import Paths
        return Paths(dikt)
    if keyword_to_type[keyword] == 'PathItem':
        from .path_item import PathItem
        return PathItem(dikt)
    if keyword_to_type[keyword] == 'Operation':
        from .operation import Operation
        return Operation(dikt)
    if keyword_to_type[keyword] == 'ExternalDocumentation':
        from .external_documentation import ExternalDocumentation
        return ExternalDocumentation(dikt)
    if keyword_to_type[keyword] == 'Parameter':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .parameter import Parameter
        return Parameter(dikt)
    if keyword_to_type[keyword] == 'RequestBody':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .request_body import RequestBody
        return RequestBody(dikt)
    if keyword_to_type[keyword] == 'Response':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .response import Response
        return Response(dikt)
    if keyword_to_type[keyword] == 'Callback':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .callback import Callback
        return Callback(dikt)
    if keyword_to_type[keyword] == 'SecurityRequirement':
        from .security_requirement import SecurityRequirement
        return SecurityRequirement(dikt)
    if keyword_to_type[keyword] == 'Schema':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .schema import Schema
        return Schema(dikt)
    if keyword_to_type[keyword] == 'Example':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .example import Example
        return Example(dikt)
    if keyword_to_type[keyword] == 'Encoding':
        from .encoding import Encoding
        return Encoding(dikt)
    if keyword_to_type[keyword] == 'Header':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .header import Header
        return Header(dikt)
    if keyword_to_type[keyword] == 'OAuthFlows':
        from .oauth_flows import OAuthFlows
        return OAuthFlows(dikt)
    if keyword_to_type[keyword] == 'OAuthFlow':
        from .oauth_flow import OAuthFlow
        return OAuthFlow(dikt)
    if keyword_to_type[keyword] == 'Discriminator':
        from .discriminator import Discriminator
        return Discriminator(dikt)
    if keyword_to_type[keyword] == 'XML':
        from .xml import XML
        return XML(dikt)
    if keyword_to_type[keyword] == 'Components':
        from .components import Components
        return Components(dikt)
    if keyword_to_type[keyword] == 'MediaType':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .media_type import MediaType
        return MediaType(dikt)
    if keyword_to_type[keyword] == 'Link':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .link import Link
        return Link(dikt)
    if keyword_to_type[keyword] == 'SecurityScheme':
        if '$ref' in dikt:
            from .reference import Reference
            return Reference(dikt)
        from .security_scheme import SecurityScheme
        return SecurityScheme(dikt)
    if keyword_to_type[keyword] == 'Tag':
        from .tag import Tag
        return Tag(dikt)
    if keyword_to_type[keyword] == 'string':
        return dikt  # in this case, dikt is just a string. This should only happen for enum and tags
    return None  # can probably make this return dikt for the extension cases


keyword_to_type = {
    # mapping keywords
    'variables': 'ServerVariable',
    'schemas': 'Schema',
    'callbacks': 'Callback',
    'mapping': 'string',
    'responses': 'Response',
    'headers': 'Header',
    'content': 'MediaType',
    'examples': 'Example',
    'encoding': 'Encoding',
    'links': 'Link',
    'parameters': 'Parameter',
    'requestBodies': 'RequestBody',
    'securitySchemes': 'SecuritySchemes',
    'scopes': 'string',

    # object keywords
    'info': 'Info',
    'contact': 'Contact',
    'license': 'License',
    'paths': 'Paths',
    '/': 'PathItem',
    'get': 'Operation',
    'put': 'Operation',
    'post': 'Operation',
    'delete': 'Operation',
    'options': 'Operation',
    'head': 'Operation',
    'patch': 'Operation',
    'trace': 'Operation',
    'externalDocs': 'ExternalDocumentation',
    'requestBody': 'RequestBody',
    'components': 'Components',
    'properties': 'Schema',  # todo: schemas
    'description': 'Schema',  # inside schemas
    'discriminator': 'Discriminator',
    'xml': 'XML',
    'schema': 'Schema',
    'flows': 'OAuthFlows',
    'implicit': 'OAuthFlow',
    'password': 'OAuthFlow',
    'clientCredentials': 'OAuthFlow',
    'authorizationCode': 'OAuthFlow',

    # array keywords
    'servers': 'Server',
    'security': 'SecurityRequirement',
    'tags': 'Tag',
    'parameters': 'Parameter',
    'op_tags': 'string',  # Operation Object tags
    'enum': 'string',
}
