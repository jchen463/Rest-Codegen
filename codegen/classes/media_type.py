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
        
    def __eq__(self, other):
        return self.schema == other.schema and self.example == other.example \
           and self.examples == other.examples and self.encoding == other.encoding \
           and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.schema != other.schema and self.example != other.example \
           and self.examples != other.examples and self.encoding != other.encoding \
           and self.extensions != other.extensions
