from .rep import Rep


class PathItem(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['summary', 'description',
                   'get', 'put', 'post',
                   'delete', 'options', 'head',
                   'patch', 'trace', 'servers',
                   'parameters', 'extensions']
        objects = ['get', 'put', 'post',
                   'delete', 'options', 'head',
                   'patch', 'trace']
        arrays = ['servers', 'parameters']

        d = parse_dict(dikt=dikt, allowed=allowed)

        self.ref = None
        if '$ref' in dikt:
            self.ref = dikt['$ref']

        self.summary = d['summary']
        self.description = d['description']
        self.get = d['get']
        self.put = d['put']
        self.post = d['post']
        self.delete = d['delete']
        self.options = d['options']
        self.head = d['head']
        self.patch = d['patch']
        self.trace = d['trace']
        self.servers = d['servers']
        self.parameters = d['parameters']
        self.extensions = d['extensions']
        
    def __eq__(self, other):
        return self.summary == other.summary and self.description == other.description \
           and self.get == other.get and self.put == other.put \
           and self.post == other.post and self.delete == other.delete \
           and self.options == other.options and self.head == other.head \
           and self.patch == other.patch and self.trace == other.trace \
           and self.servers == other.servers and self.parameters == other.parameters \
           and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.summary != other.summary and self.description != other.description \
           and self.get != other.get and self.put != other.put \
           and self.post != other.post and self.delete != other.delete \
           and self.options != other.options and self.head != other.head \
           and self.patch != other.patch and self.trace != other.trace \
           and self.servers != other.servers and self.parameters != other.parameters \
           and self.extensions != other.extensions
