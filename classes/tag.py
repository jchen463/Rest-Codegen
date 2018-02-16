class Tag:
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
