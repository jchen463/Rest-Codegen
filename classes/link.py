import parse


class Link:
    def __init__(self, dikt):
        # !!! parameters and requestBody can be <any | {expression}>
        # probably will have to manually input parameters and requestBody
        allowed = ['operationRef', 'operationId', 'parameters',
                   'requestBody', 'description', 'server',
                   'extensions']
        objects = ['server']
        mappings = ['parameters']

        d = parse_dict(dikt=dikt, allowed=allowed, objects=objects,
                       mappings=mappings)

        self.operationRef = d['operationRef']
        self.operationId = d['operationId']
        self.parameters = d['parameters']
        self.requestBody = d['requestBody']
        self.description = d['description']
        self.server = d['server']
        self.extensions = d['extensions']
