from .rep import Rep


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

        d = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, objects=objects)

        self.type = d['type']
        self.description = d['description']
        self.name = d['name']
        self._in = d['in']
        self.scheme = d['scheme']
        self.bearerFormat = d['bearerFormat']
        self.flows = d['flows']
        self.openIdConnectUrl = d['openIdConnectUrl']
        self.extensions = d['extensions']
