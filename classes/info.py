from .parse import parse_dict


class Info:
    def __init__(self, dikt):
        allowed = ['title', 'description', 'termsOfService',
                   'contact', 'license', 'version',
                   'extensions']
        required = ['title', 'version']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required)

        self.title = d['title']
        self.description = d['description']
        self.termsOfService = d['termsOfService']
        self.contact = d['contact']
        self.license = d['license']
        self.version = d['version']
        self.extensions = d['extensions']
