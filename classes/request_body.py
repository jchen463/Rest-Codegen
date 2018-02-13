from parse import parse_dict


class RequestBody:
    def __init__(self, dikt):
        allowed = ['description', 'content', 'required']
        mappings = ['content']
        booleans = ['required']
        d = parse_dict(dikt=dikt, allowed=allowed, mappings=mappings, booleans=booleans)
        for key, value in d.items():
            self.key = value
