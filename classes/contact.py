from .parse import parse_dict


class Contact:
    def __init__(self, dikt):
        allowed = ['name', 'url', 'email', 'extensions']

        d = parse_dict(dikt=dikt, allowed=allowed)

        self.name = d['name']
        self.url = d['url']
        self.email = d['email']
        self.extensions = d['extensions']
