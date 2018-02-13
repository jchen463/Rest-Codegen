from parse import parse_dict


class ServerVariable:
    def __init__(self, dikt):
        # !!! enum is an array
        allowed = ['enum', 'default', 'description']
        required = ['default']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required)
        for key, value in d.items():
            self.key = value
