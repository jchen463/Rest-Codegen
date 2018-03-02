from .rep import Rep


class ExternalDocumentation(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['description', 'url', 'extensions']
        required = ['url']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required)

        self.description = d['description']
        self.url = d['url']
        self.extensions = d['extensions']
        
    def __eq__(self, other):
        return self.description == other.description and self.url == other.url \
           and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.description != other.description and self.url != other.url \
           and self.extensions != other.extensions
