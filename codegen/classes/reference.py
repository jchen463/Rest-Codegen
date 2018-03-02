from .rep import Rep


class Reference(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['$ref']
        required = ['$ref']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required)
        self.ref = d['$ref']
        
    def __eq__(self, other):
        return self.ref == other.ref
 
    def __ne__(self, other):
        return self.ref != other.ref
