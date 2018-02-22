from .rep import Rep


class MediaType(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['schema', 'example', 'examples',
                   'encoding', 'extensions']
        objects = ['schema']
        mappings = ['examples', 'encoding']

        d = parse_dict(dikt=dikt, allowed=allowed, objects=objects,
                       mappings=mappings)

        self.schema = d['schema']
        self.example = d['example']
        self.examples = d['examples']
        self.encoding = d['encoding']
        self.extensions = d['extensions']
