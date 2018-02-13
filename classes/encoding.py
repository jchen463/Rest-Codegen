import parse


class Encoding:
    def __init__(self, dikt):
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
