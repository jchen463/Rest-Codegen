from parse import parse_dict


class Info:
    def __init__(self, dikt):
        allowed = ['title', 'description', 'termsOfService', 'contact', 'license', 'version']  # fields that are allowed
        required = ['title', 'version']  # fields that are required
        d = parse_dict(dikt=dikt, allowed=allowed, required=required)
        for key, value in d.items():
            self.key = value
