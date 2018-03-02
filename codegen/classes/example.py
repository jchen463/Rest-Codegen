from .rep import Rep


class Example(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['summary', 'description', 'value',
                   'externalValue', 'extensions']

        d = parse_dict(dikt=dikt, allowed=allowed)

        self.summary = d['summary']
        self.description = d['description']
        self.value = d['value']
        self.externalValue = d['externalValue']
        self.extensions = d['extensions']

    def __eq__(self, other):
        return self.summary == other.summary and self.description == other.description \
           and self.value == other.value and self.externalValue == other.externalValue \
           and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.summary != other.summary and self.description != other.description \
           and self.value != other.value and self.externalValue != other.externalValue \
           and self.extensions != other.extensions
