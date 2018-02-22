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
