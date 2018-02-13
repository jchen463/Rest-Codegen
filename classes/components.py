from parse import parse_dict


class Components:
    def __init__(self, dikt):
        allowed = ['schemas', 'responses', 'parameters', 'examples',
                   'requestBodies', 'headers', 'securitySchemes', 'links', 'callbacks']
        mappings = ['schemas', 'responses', 'parameters', 'examples',
                    'requestBodies', 'headers', 'securitySchemes', 'links', 'callbacks']
        d = parse_dict(dikt=dikt, allowed=allowed, mappings=mappings)
        for key, value in d.items():
            self.key = value
