from .rep import Rep


class Encoding(Rep):
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
        
    def __eq__(self, other):
        return self.contentType == other.contentType and self.headers == other.headers \
           and self.style == other.style and self.explode == other.explode \
           and self.allowReserved == other.allowReserved and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.contentType != other.contentType and self.headers != other.headers \
           and self.style != other.style and self.explode != other.explode \
           and self.allowReserved != other.allowReserved and self.extensions != other.extensions
