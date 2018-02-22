from .rep import Rep


class RequestBody(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

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
