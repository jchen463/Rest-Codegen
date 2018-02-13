from parse import parse_dict


class Discriminator:
    def __init__(self, dikt):
        allowed = ['propertyName', 'mapping']  # fields that are allowed
        required = ['propertyName']  # fields that are required
        mappings = ['mapping']  # fields that are mappings
        d = parse_dict(dikt=dikt, allowed=allowed, required=required, mappings=mappings)
        for key, value in d.items():
            self.key = value
