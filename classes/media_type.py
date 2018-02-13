from parse import parse_dict


class MediaType:
    def __init__(self, dikt):
        # !!! example is <any>
        allowed = ['schema', 'example', 'examples',
                   'encoding']  # fields that are allowed
        mappings = ['examples', 'encoding']
        objects = ['schema']
        d = parse_dict(dikt=dikt, allowed=allowed,
                       mappings=mappings, objects=objects)
        for key, value in d.items():
            self.key = value
