from parse import parse_dict


class Contact:
    def __init__(self, dikt):
        allowed = ['name', 'url', 'email']
        d = parse_dict(dikt=dikt, allowed=allowed)
        for key, value in d.items():
            self.key = value
