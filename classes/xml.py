from parse import parse_dict


class XML:
    def __init__(self, dikt):
        allowed = ['name', 'namespace', 'prefix', 'attribute', 'wrapped']
        required = ['name']
        booleans = ['attribute', 'wrapped']
        d = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, booleans=booleans)
        for key, value in d.items():
            self.key = value
