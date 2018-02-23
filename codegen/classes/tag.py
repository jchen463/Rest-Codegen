from .rep import Rep


class Tag(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['name', 'description', 'externalDocs', 'extensions']
        required = ['name']
        objects = ['externalDocs']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects)

        self.name = d['name']
        self.description = d['description']
        self.externalDocs = d['externalDocs']
        self.extensions = d['extensions']

    def __eq__(self, other):
        return self.name == other.name and self.description == other.description \
           and self.externalDocs == other.externalDocs and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.name != other.name and self.description != other.description \
           and self.externalDocs != other.externalDocs and self.extensions != other.extensions
