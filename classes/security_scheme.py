from .parse import parse_dict


class SecurityScheme:
    def __init__(self, dikt):
        allowed = ['type', 'description', 'name',
                   'in', 'scheme', 'bearerFormat',
                   'flows', 'openIdConnectUrl', 'extensions']
        required = ['type', 'name', 'in',
                    'scheme', 'flows', 'openIdConnectUrl']
        objects = ['flows']

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
