from .rep import Rep


class OAuthFlow(Rep):
    def __init__(self, dikt, flow_name):
        from .parse import parse_dict

        allowed = ['authorizationCode', 'tokenUrl',
                   'refreshUrl', 'scopes', 'extensions']
        required = ['scopes']
        mappings = ['scopes']

        flows_requiring_tokenUrl = ['password',
                                    'clientCredentials', 'authorizationCode']
        flows_requiring_authorizationUrl = ['implicit', 'authorizationCode']
        if flow_name in flows_requiring_tokenUrl:
            required.append('tokenUrl')
        if flow_name in flows_requiring_authorizationUrl:
            required.append('authorizationUrl')

        d = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, mappings=mappings)

        # don't use this, because we may want functions that modify these attributes. explicit is better than implicit?
        # for key, value in d.items():
        #     setattr(self, key, value)

        self.authorizationCode = d['authorizationCode']
        self.tokenUrl = d['tokenUrl']
        self.refreshUrl = d['refreshUrl']
        self.scopes = d['scopes']
        self.extensions = d['extensions']


class OAuthFlows(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['extensions']

        d = parse_dict(dikt=dikt, allowed=allowed)
        self.extensions = d['extensions']

        self.implicit = None
        self.password = None
        self.clientCredentials = None
        self.authorizationCode = None

        if 'implicit' in dikt:
            self.implicit = OAuthFlow(dikt['implicit'], 'implicit')
        if 'password' in dikt:
            self.password = OAuthFlow(dikt['password'], 'password')
        if 'clientCredentials' in dikt:
            self.clientCredentials = OAuthFlow(
                dikt['clientCredentials'], 'clientCredentials')
        if 'authorizationCode' in dikt:
            self.authorizationCode = OAuthFlow(
                dikt['authorizationCode'], 'authorizationCode')
