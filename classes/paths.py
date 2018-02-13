from parse import parse_dict


class Paths:
    def __init__(self, dikt):
        allowed = ['/']
        d = parse_dict(dikt=dikt, allowed=allowed)
        for key, value in d.items():
            self.key = value
