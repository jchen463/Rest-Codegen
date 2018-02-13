from parse import parse_dict


class Operation:
    def __init__(self, dikt):
        # !!! tags is [<string>], other attributes are also arrays
        allowed = ['tags', 'summary', 'description',
                   'externalDocs', 'operationId', 'parameters', 'requestBody', 'responses', 'callbacks', 'deprecated', 'security', 'servers']
        required = ['responses']
        objects = ['externalDocs', 'parameters', 'requestBody',
                   'responses', 'security', 'servers']
        mappings = ['callbacks']
        booleans = ['deprecated']
        d = parse_dict(dikt=dikt, allowed=allowed, objects=objects)
        for key, value in d.items():
            self.key = value
