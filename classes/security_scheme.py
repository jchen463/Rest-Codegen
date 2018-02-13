from parse import parse_dict


class SecurityScheme:
    def __init__(self, dikt):
        allowed = ['type', 'description', 'name', 'in', 'scheme', 'bearerFormat', 'flows', 'openIdConnectUrl']
        required = ['type', 'name', 'in', 'scheme', 'flows', 'openIdConnectUrl']
        objects = ['flows']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required, objects=objects)
        for key, value in d.items():
            self.key = value
