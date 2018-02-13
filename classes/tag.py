from parse import parse_dict


class Tag:
    def __init__(self, dikt):
        allowed = ['name', 'description', 'externalDocs']
        required = ['name']
        objects = ['externalDocs']
        d = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, objects=objects)
        for key, value in d.items():
            self.key = value
