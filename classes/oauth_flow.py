from parse import parse_dict


class OAuthFlow:
    def __init__(self, dikt):
        allowed = ['authorizationUrl', 'tokenUrl', 'refreshUrl',
                   'scopes']  # fields that are allowed
        required = ['authorizationUrl', 'tokenUrl', 'scopes']
        mappings = ['scopes']
        d = parse_dict(dikt=dikt, allowed=allowed, required=required
                       mappings=mappings)
        for key, value in d.items():
            self.key = value
