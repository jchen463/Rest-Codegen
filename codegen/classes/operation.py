from .rep import Rep


class Operation(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

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
        
    def __eq__(self, other):
        return self.summary == other.summary and self.description == other.description \
           and self.externalDocs == other.externalDocs and self.operationId == other.operationId \
           and self.parameters == other.parameters and self.requestBody == other.requestBody \
           and self.callbacks == other.callbacks and self.deprecated == other.deprecated \
           and self.security == other.security and self.servers == other.servers \
           and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.summary != other.summary and self.description != other.description \
           and self.externalDocs != other.externalDocs and self.operationId != other.operationId \
           and self.parameters != other.parameters and self.requestBody != other.requestBody \
           and self.callbacks != other.callbacks and self.deprecated != other.deprecated \
           and self.security != other.security and self.servers != other.servers \
           and self.extensions != other.extensions
