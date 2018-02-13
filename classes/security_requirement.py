class SecurityRequirement:
    def __init__(self, dikt):
        for key, value in dikt.items():
            self.name = key
            self.array = value
