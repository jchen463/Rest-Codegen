from parse import parse_dict


class Server:
    def __init__(self, dikt):
        allowed = ['url', 'description', 'variables']
        required = ['url']
        mappings = ['variables']
        d = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, mappings=mappings)
        for key, value in d.items():
            self.key = value
