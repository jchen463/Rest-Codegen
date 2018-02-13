from parse import parse_dict


class ExternalDocumentation:
    def __init__(self, dikt):
        allowed = ['description', 'url']  # fields that are allowed
        required = ['url']  # fields that are required
        d = parse_dict(dikt=dikt, allowed=allowed, required=required)
        for key, value in d.items():
            self.key = value
