class Reference:
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['$ref']
        required = ['$ref']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required)
        self.ref = d['$ref']
