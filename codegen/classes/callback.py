from .rep import Rep


class Callback(Rep):
    def __init__(self, dikt):
        from .parse import ext_regex

        self.dikt = {}
        self.extensions = []
        for key, value in dikt.items():
            if ext_regex.match(key):
                self.extensions.append({key, value})
            else:
                self.dikt[key] = value
    def __eq__(self, other):
        return self.dikt == other.dikt and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.dikt != other.dikt or self.extensions != other.extensions
