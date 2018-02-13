import parse


class Paths:
    def __init__(self, dikt):
        self.dikt = {}
        self.extensions = []
        for key, value in dikt.items():
            if parse.ext_regex.match(key):
                self.extensions.append({key: value})
            else:
                self.dikt[key] = parse.get_object('/', value)
