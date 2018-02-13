from .parse import parse_dict


class Operation:
    def __init__(self, dikt):
        allowed = ['summary', 'description', 'externalDocs',
                   'operationId', 'parameters', 'requestBody',
                   'responses', 'callbacks', 'deprecated',
                   'security', 'servers', 'extensions']
        required = ['responses']
        objects = ['externalDocs', 'requestBody']
        mappings = ['callbacks']
        arrays = ['parameters', 'security', 'servers']
        booleans = ['deprecated']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects, mappings=mappings, booleans=booleans,
                       arrays=arrays)

        if 'tags' in dikt:
            self.tags = parse.get_array('op_tags', dikt['tags'])
        else:
            self.tags = None

        self.responses = {}
        for key, value in dikt['responses']:
            self.responses[key] = parse.get_object('responses', value)

        self.summary = d['summary']
        self.description = d['description']
        self.externalDocs = d['externalDocs']
        self.operationId = d['operationId']
        self.parameters = d['parameters']
        self.requestBody = d['requestBody']
        self.callbacks = d['callbacks']
        self.deprecated = d['deprecated']
        self.security = d['security']
        self.servers = d['servers']
        self.extensions = d['extensions']
