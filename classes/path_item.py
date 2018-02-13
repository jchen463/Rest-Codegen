from .parse import parse_dict


class PathItem:
    def __init__(self, dikt):
        allowed = ['$ref', 'summary', 'description',
                   'get', 'put', 'post',
                   'delete', 'options', 'head',
                   'patch', 'trace', 'servers',
                   'parameters', 'extensions']
        objects = ['get', 'put', 'post',
                   'delete', 'options', 'head',
                   'patch', 'trace']
        arrays = ['servers', 'parameters']

        d = parse_dict(dikt=dikt, allowed=allowed)

        self.ref = d['$ref']
        self.summary = d['summary']
        self.description = d['description']
        self.get = d['get']
        self.put = d['put']
        self.post = d['post']
        self.delete = d['delete']
        self.options = d['options']
        self.head = d['head']
        self.patch = d['patch']
        self.trace = d['trace']
        self.servers = d['servers']
        self.parameters = d['parameters']
        self.extensions = d['extensions']
