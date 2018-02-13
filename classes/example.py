from parse import parse_dict


class Example:
    def __init__(self, dikt):
        # !!! 'value' field is <any>
        allowed = ['summary', 'description', 'value',
                   'externalValue']  # fields that are allowed
        d = parse_dict(dikt=dikt, allowed=allowed)
        for key, value in d.items():
            self.key = value
