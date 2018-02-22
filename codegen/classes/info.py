from .rep import Rep


class Info(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict
        allowed = ['title', 'description', 'termsOfService',
                   'contact', 'license', 'version',
                   'extensions']
        required = ['title', 'version']
        objects = ['contact', 'license']

        d = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, objects=objects)

        self.title = d['title']
        self.description = d['description']
        self.termsOfService = d['termsOfService']
        self.contact = d['contact']
        self.license = d['license']
        self.version = d['version']
        self.extensions = d['extensions']
