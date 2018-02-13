import parse


class Components:
    def __init__(self, dikt):
        allowed = ['schemas', 'responses', 'parameters',
                   'examples', 'requestBodies', 'headers',
                   'securitySchemes', 'links', 'callbacks',
                   'extensions']
        mappings = ['schemas', 'responses', 'parameters',
                    'examples', 'requestBodies', 'headers',
                    'securitySchemes', 'links', 'callbacks']

        d = parse_dict(dikt=dikt, allowed=allowed, mappings=mappings)

        self.schemas = d['schemas']
        self.responses = d['responses']
        self.parameters = d['parameters']
        self.examples = d['examples']
        self.requestBodies = d['requestBodies']
        self.headers = d['headers']
        self.securitySchemes = d['securitySchemes']
        self.links = d['links']
        self.callbacks = d['callbacks']
        self.extensions = d['extensions']
