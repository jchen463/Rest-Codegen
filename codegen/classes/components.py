from .rep import Rep


class Components(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

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
        
    def __eq__(self, other):
        return self.schemas == other.schemas and self.responses == other.responses \
           and self.parameters == other.parameters and self.examples == other.examples \
           and self.requestBodies == other.requestBodies and self.headers == other.headers \
           and self.securitySchemes == other.securitySchemes and self.links == other.links \
           and self.callbacks == other.callbacks and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.schemas != other.schemas and self.responses != other.responses \
           and self.parameters != other.parameters and self.examples != other.examples \
           and self.requestBodies != other.requestBodies and self.headers != other.headers \
           and self.securitySchemes != other.securitySchemes and self.links != other.links  \
           and self.callbacks != other.callbacks and self.extensions != other.extensions
