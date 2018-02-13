import parse


class OAuthFlow:
    def __init__(self, dikt):
        allowed = ['authorizationUrl', 'tokenUrl', 'refreshUrl',
                   'scopes', 'extensions']
        required = ['authorizationUrl', 'tokenUrl', 'scopes']
        mappings = ['scopes']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required
                       mappings=mappings)

        self.authorizationUrl = d['authorizationUrl']
        self.tokenUrl = d['tokenUrl']
        self.refreshUrl = d['refreshUrl']
        self.scopes = d['scopes']
        self.extensions = d['extensions']
