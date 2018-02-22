from .rep import Rep


class Response(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['description', 'headers', 'content',
                   'links', 'extensions']
        required = ['description']
        mappings = ['headers', 'content', 'links']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       mappings=mappings)

        self.description = d['description']
        self.headers = d['headers']
        self.content = d['content']
        self.links = d['links']
        self.extensions = d['extensions']
