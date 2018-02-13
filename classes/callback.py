from parse import parse_callback


class Callback:
    def __init__(self, dikt):
        self.dikt = {}
        d = parse_callback(dikt)
        for key, value in d.items():
            self.dikt[key] = value
