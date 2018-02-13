from .parse import parse_dict


class OAuthFlows:
    def __init__(self, dikt):
        allowed = ['implicit', 'password', 'clientCredentials',
                   'authorizationCode', 'extensions']
        objects = ['implicit', 'password', 'clientCredentials',
                   'authorizationCode']

        d = parse_dict(dikt=dikt, allowed=allowed, objects=objects)

        self.implicit = d['implicit']
        self.password = d['password']
        self.clientCredentials = d['clientCredentials']
        self.authorizationCode = d['authorizationCode']
        self.extensions = d['extensions']
