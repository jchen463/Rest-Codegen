from parse import parse_dict


class Response:
    def __init__(self, dikt):
        allowed = ['description', 'headers', 'content', 'links']
        required = ['description']
        mappings = ['headers', 'content', 'links']
        booleans = ['required']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required, mappings=mappings, booleans=booleans)
        for key, value in d.items():
            self.key = value
