class Callback:
    def __init__(self, dikt):
        from .parse import ext_regex

        self.dikt = {}
        self.extensions = []
        for key, value in dikt.items():
            if ext_regex.match(key):
                self.extensions.append({key, value})
            else:
                self.dikt[key] = value
