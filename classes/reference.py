class Reference:
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['$ref']
        required = ['$ref']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required)
        for key, value in d.items():
            self.key = value
