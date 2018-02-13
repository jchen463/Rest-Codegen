from .parse import parse_dict


class ServerVariable:
    def __init__(self, dikt):
        allowed = ['enum', 'default', 'description', 'extensions']
        required = ['default']
        arrays = ['enum']

        d = parse_dict(dikt=dikt, allowed=allowed)

        self.enum = d['enum']
        self.default = d['default']
        self.description = d['description']
        self.extensions = d['extensions']
