def parse_dict(dikt, allowed, required=[], objects=[], mappings=[], booleans=[], arrays=[], anys=[]):
    d = {}
    for attr in required:
        if attr not in dikt:
            raise ValueError('required field ' + attr + ' is missing')
    for attr in allowed:
        d[attr] = None

    for key, value in dikt.items():
        if key in objects:
            d[key] = get_object(key, value)
        elif key in mappings:
            d[key] = get_mapping(key, value)
        elif key in arrays:  # server: [<Server Object>]
            d[key] = get_array(key, value)
        # elif key in booleans:
        #     d[key] = get_boolean(key, value)
        else:  # string
            d[key] = value

    for key, value in d.items():
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
            mapping[key] = get_object(keyword_to_type[keyword], value)

    return mapping


def get_array(keyword, arr):
    array = []  # list

    for dikt in arr:
        array.append(get_object(keyword_to_type[keyword], dikt))

    return array


def get_object(keyword, dikt):
    if keyword_to_type[keyword] == 'Info':
        from info import Info
        return Info(dikt)
    if keyword_to_type[keyword] == 'Contact':
        from contact import Contact
        return Contact(dikt)
    if keyword_to_type[keyword] == 'License':
        from license_spec import License
        return License(dikt)
    if keyword_to_type[keyword] == 'Info':
        from info import Info
        return Info(dikt)

    return None


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
    'responses': 'Responses',  # may need special care
    'default': 'Response',  # responses
    'components': 'Components',
    'properties': 'Schema',
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
    'tags': 'string'  # Operation Object tags






    # {expression}: <Path Item Object>
    # {name}: [<string>]

    # not handling booleans

}


def parse_callback(dikt):
    d = {}
    for key, value in dikt.items():
        d[key] = PathItem(value)
    return d

# def parse_headers(dikt):
#     headers = {}
#     for key, value in dikt.items():
#         headers[key] = Header(value)

#     return headers


# def parse_variables(dikt):
#     variables
