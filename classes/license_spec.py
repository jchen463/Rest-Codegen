import parse


class License:
    def __init__(self, dikt):
        allowed = ['name', 'url', 'extensions']
        required = ['name']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required)

        self.name = d['name']
        self.url = d['url']
        self.extensions = d['extensions']
