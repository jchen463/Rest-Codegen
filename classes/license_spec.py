from parse import parse_dict


class License:
    def __init__(self, dikt):
        allowed = ['name', 'url']  # fields that are allowed
        required = ['name']  # fields that are required
        d = parse_dict(dikt=dikt, allowed=allowed, required=required)
        for key, value in d.items():
            self.key = value
