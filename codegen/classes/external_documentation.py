class ExternalDocumentation:
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['description', 'url', 'extensions']
        required = ['url']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required)

        self.description = d['description']
        self.url = d['url']
        self.extensions = d['extensions']
