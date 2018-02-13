from parse import parse_dict


class Link:
    def __init__(self, dikt):
        # !!! requestBody is <any> | {expression} may need specialized processing
        allowed = ['operationRef', 'operationId', 'parameters', 'requestBody', 'description', 'server']  # fields that are allowed
        mappings = ['parameters']
        d = parse_dict(dikt=dikt, allowed=allowed, mappings=mappings)
        for key, value in d.items():
            self.key = value
