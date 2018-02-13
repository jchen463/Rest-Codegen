from parse import parse_dict


class OAuthFlows:
    def __init__(self, dikt):
        allowed = ['implicit', 'password', 'clientCredentials',
                   'authorizationCode']
        objects = ['implicit', 'password', 'clientCredentials',
                   'authorizationCode']
        d = parse_dict(dikt=dikt, allowed=allowed, objects=objects)
        for key, value in d.items():
            self.key = value
