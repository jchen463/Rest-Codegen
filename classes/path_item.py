from .parse import parse_dict


class PathItem:
    def __init__(self, dikt):
        # !!! servers and parameters are arrays
        allowed = ['$ref', 'summary', 'description',
                   'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'security', 'servers']
        required = ['responses']
        objects = ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace', 'servers', 'parameters']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required, objects=objects)
        for key, value in d.items():
            self.key = value
