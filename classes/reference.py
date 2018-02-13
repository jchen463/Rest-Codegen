from .parse import parse_dict


class Reference:
    def __init__(self, dikt):
        allowed = ['$ref']
        required = ['$ref']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required)
        for key, value in d.items():
            self.key = value


class A:
    def __init__(self):
        x = ['a', 'b', 'c']
        for item in x:
            self.item = 5
