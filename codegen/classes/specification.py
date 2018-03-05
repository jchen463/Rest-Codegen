from .rep import Rep


class Specification(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        allowed = ['openapi', 'info', 'servers', 'paths',
                   'components', 'security', 'tags', 'externalDocs']
        required = ['openapi', 'info', 'paths']
        objects = ['info', 'paths', 'components', 'externalDocs']
        arrays = ['servers', 'security', 'tags']

        d = parse_dict(dikt=dikt, allowed=allowed,
                       required=required, objects=objects, arrays=arrays)

        self.openapi = d['openapi']
        self.info = d['info']
        self.servers = d['servers']
        self.paths = d['paths']
        self.components = d['components']
        self.security = d['security']
        self.tags = d['tags']
        self.externalDocs = d['externalDocs']

    def __eq__(self, other):
        return self.openapi == other.openapi and self.info == other.info \
            and self.servers == other.servers and self.paths == other.paths \
            and self.components == other.components and self.security == other.security \
            and self.tags == other.tags and self.externalDocs == other.externalDocs

    def __ne__(self, other):
        return self.openapi != other.openapi and self.info != other.info \
            and self.servers != other.servers and self.paths != other.paths \
            and self.components != other.components and self.security != other.security \
            and self.tags != other.tags and self.externalDocs != other.externalDocs
