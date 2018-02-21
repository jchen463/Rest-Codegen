class Encoding:
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['contentType', 'headers', 'style',
                   'explode', 'allowReserved', 'extensions']
        mappings = ['headers']
        booleans = ['explode', 'allowReserved']

        d = parse_dict(dikt=dikt, allowed=allowed)

        self.contentType = d['contentType']
        self.headers = d['headers']
        self.style = d['style']
        self.explode = d['explode']
        self.allowReserved = d['allowReserved']
        self.extensions = d['extensions']
