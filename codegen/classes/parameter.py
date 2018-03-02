from .rep import Rep


class Parameter(Rep):
    def __init__(self, dikt):
        from .parse import parse_dict

        if 'content' in dikt != 'schema' in dikt:
            raise ValueError('REQUIRED: one of \'content\' or \'schema\' only')
        if 'example' in dikt != 'examples' in dikt:
            raise ValueError(
                'REQUIRED: one of \'example\' or \'examples\' only')

        allowed = ['name', 'in', 'description',
                   'required', 'deprecated', 'allowEmptyValue',
                   'style', 'explode', 'allowReserved',
                   'schema', 'examples',
                   'content', 'extensions']
        required = ['name', 'in']
        booleans = ['required', 'deprecated', 'allowEmptyValue'
                    'explode', 'allowReserved']
        mappings = ['content', 'examples']
        objects = ['schema']

        if dikt['in'] == 'path':
            required.append('required')

        # Default values
        # self.explode = False
        # if 'style' in dikt and dikt['style'] == 'form':
        # #     self.explode = True
        # self.required = False
        # self.allowReserved = False

        # <any>
        if 'example' in dikt:
            self.example = dikt['example']

        d = parse_dict(dikt=dikt, allowed=allowed, required=required,
                       objects=objects, mappings=mappings, booleans=booleans, arrays=arrays)

        self.name = d['name']
        self._in = d['in']
        self.description = d['description']
        self.required = d['required']
        self.deprecated = d['deprecated']
        self.style = d['style']
        self.explode = d['explode']
        self.allowReserved = d['allowReserved']
        self.schema = d['schema']
        self.examples = d['examples']
        self.content = d['content']
        self.extensions = d['extensions']
        
    def __eq__(self, other):
        return self.name == other.name and self._in == other._in \
           and self.description == other.description and self.required == other.required \
           and self.deprecated == other.deprecated and self.style == other.style \
           and self.explode == other.explode and self.allowReserved == other.allowReserved \
           and self.schema == other.schema and self.examples == other.examples \
           and self.content == other.content and self.extensions == other.extensions
 
    def __ne__(self, other):
        return self.name != other.name and self._in != other._in \
           and self.description != other.description and self.required != other.required \
           and self.deprecated != other.deprecated and self.style != other.style \
           and self.explode != other.explode and self.allowReserved != other.allowReserved \
           and self.schema != other.schema and self.examples != other.examples \
           and self.content != other.content and self.extensions != other.extensions

    """
    Rules for serialization of parameter:
    For simple scenarios, a 'schema' and 'style' can describe the structure and syntax of the parameter
    For complex scenarios, the content property can define the media type and schema of the parameter
    A parameter MUST contain either a schema property or a content property, but not both.
    When example or examples is provided along with the schema object, the example MUST follow the prescribed serialization strategy for the parameter
    """
