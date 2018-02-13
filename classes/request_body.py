import parse


class RequestBody:
    def __init__(self, dikt):
        allowed = ['description', 'content', 'required',
                   'extensions']
        required = ['content']
        mappings = ['content']
        booleans = ['required']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       mappings=mappings, booleans=booleans)

        self.description = d['description']
        self.content = d['content']
        self.required = d['required']
        self.extensions = d['extensions']
