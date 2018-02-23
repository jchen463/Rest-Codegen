from .rep import Rep


class Link(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict
        from .parse import get_mapping

        allowed = ['operationRef', 'operationId',
                   'requestBody', 'description', 'server',
                   'extensions']
        objects = ['server']

        d = parse_dict(dikt=dikt, allowed=allowed, objects=objects,
                       mappings=mappings)

        self.operationRef = d['operationRef']
        self.operationId = d['operationId']
        self.requestBody = d['requestBody']
        self.description = d['description']
        self.server = d['server']
        self.extensions = d['extensions']

        self.parameters = None
        if 'parameters' in dikt:
            self.parameters = get_mapping('scopes', dikt['parameters'])
            
    def __eq__(self, other):
        return self.operationRef == other.operationRef and self.operationId == other.operationId \
           and self.requestBody == other.requestBody and self.description == other.description \
           and self.server == other.server and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.operationRef != other.operationRef and self.operationId != other.operationId \
           and self.requestBody != other.requestBody and self.description != other.description \
           and self.server != other.server and self.extensions != other.extensions

        # !!! parameters and requestBody can be <any | {expression}>
