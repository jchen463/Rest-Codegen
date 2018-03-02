from .rep import Rep


class SecurityRequirement(Rep):
    def __init__(self, dikt):
        for key, value in dikt.items():
            self.name = key
            self.array = value
            
    def __eq__(self, other):
        return self.name == other.name and self.array == other.array
 
    def __ne__(self, other):
        return self.name != other.name and self.array != other.array
