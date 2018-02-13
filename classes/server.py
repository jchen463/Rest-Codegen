import parse


class Server:
    def __init__(self, dikt):
        allowed = ['url', 'description', 'variables', 'extensions']
        required = ['url']
        mappings = ['variables']

        d = parse_dict(dikt=dikt, allowed=allowed)

        self.url = d['url']
        self.description = d['description']
        self.variables = d['variables']
        self.extensions = d['extensions']
