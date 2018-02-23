from .rep import Rep


class XML(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['name', 'namespace', 'prefix',
                   'attribute', 'wrapped', 'extensions']
        required = ['name']
        booleans = ['attribute', 'wrapped']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       booleans=booleans)

        self.name = d['name']
        self.namespace = d['namespace']
        self.prefix = d['prefix']
        self.attribute = d['attribute']
        self.wrapped = d['wrapped']
        self.extensions = d['extensions']
        
    def __eq__(self, other):
        return self.name == other.name and self.namespace == other.namespace \
           and self.prefix == other.prefix and self.attribute == other.attribute \
           and self.wrapped == other.wrapped and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.name != other.name and self.namespace != other.namespace \
           and self.prefix != other.prefix and self.attribute != other.attribute \
           and self.wrapped != other.wrapped and self.extensions != other.extensions
