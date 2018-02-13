from parse import parse_dict


class Encoding:
    def __init__(self, dikt):
        allowed = ['contentType', 'headers', 'style', 'explode', 'allowReserved']  # fields that are allowed
        mappings = ['mapping']  # fields that are mappings
        booleans = ['explode', 'allowReserved']  # fields that are booleans
        d = parse_dict(dikt=dikt, allowed=allowed, mappings=mappings, booleans=booleans)
        for key, value in d.items():
            self.key = value
