import re

import codegen.codegen_config as cfg


class OpenAPI3():
    ext_regex = re.compile('x-.*')

    @staticmethod
    def get_reference(dikt):
        if '$ref' not in dikt:
            return dikt

        ref_string = dikt['$ref']
        ref_path = ref_string.split('/')

        ref = cfg.SPEC_DICT[ref_path[1]][ref_path[2]][ref_path[3]]
        return ref

    @staticmethod
    def get_extensions(dikt):
        extensions = None

        for key, value in dikt.items():
            if ext_regex.match(key):
                extensions = {}
                break
            return None

        for key, value in dikt.items():
            if ext_regex.match(key):
                extensions[key] = value

        return extensions

    @staticmethod
    def get_contents(dikt):
        if 'content' not in dikt:
            return None

        content = []
        for format, info in dikt.items():
            contents.append(Content(format, info))

        return contents

    @staticmethod
    def get_content_formats(dikt):
        contents = get_content(dikt)
        if contents is None:
            return None

        formats = []
        for content in contents:
            formats.append(content.format)

        return formats

    @staticmethod
    def get_content_types(dikt):
        contents = get_content(dikt)
        if contents is None:
            return None

        types = []
        for content in contents:
            types.append(content.type)

        return types

    @staticmethod
    def get_schema_type(dikt):
        schema_dict = dikt.get('schema')
        if schema_dict is None:
            return None

        def get_type(schema_dict, depth=0):
            if (schema_dict.get('$ref')):
                s = ref.split('/')[3]
                for _ in range(depth):
                    s += '>'
                return s
            if schema_dict.get('type') == 'array':
                return 'array<' + get_type(schema_dict['items'], depth + 1)
            # TODO OBJECTS
            # TODO FORMAT
            s = schema_dict['type']
            for _ in range(depth):
                s += '>'
            return s

        return get_type(schema_dict)

    @staticmethod
    def to_boolean(s):
        if s is None:
            return False  # or should we return None?
        if s.lower() == 'true':
            return True
        return False


class Path(OpenAPI3):
    """
    description, summary, servers, parameters, extensions can be from higher level
    paths have references, but not sure if we're going to support it because seems like openapi3 doesn't support it either?
    highest level extensions aren't supported (i.e. paths -> ^x-)
    """

    def __init__(self, parent_dict, method, operation_dict):
        path_dict = merge_dicts(parent_dict, operation_dict)
        self.url = path_dict.get('url')
        self.tag = get_tag(path_dict)
        self.method = method
        self.function_name = path_dict.get('operationId')
        # self.200_response_schema =
        self.parameters = get_parameters(path_dict)  # array<Parameter>
        self.parameters_in = get_parameters_in()  # set<string>
        self.request_body = get_request_body(path_dict)
        self.responses = get_responses(path_dict)  # REQUIRED {<string>, Response}
        self.response_formats = get_response_formats()  # array<string>
        self.dependencies = get_dependencies()  # array<string> TODO can be in parameters, request body, responses

        self.summary = path_dict.get('summary')
        self.description = path_dict.get('description')
        self.externalDocs = path_dict.get('externalDocs')  # TODO
        self.callbacks = path_dict.get('callbacks')  # TODO
        self.security = path_dict.get('security')  # TODO
        self.servers = path_dict.get('servers')  # TODO
        self.deprecated = to_boolean(path_dict.get('deprecated'))
        self.extensions = get_extensions(path_dict)

    @staticmethod
    def get_tag(path_dict):
        tags = path_dict.get('tags')
        if tags is None:
            return None
        return tags[0]

    def get_response_formats(self):
        # self.responses will never be None
        response_formats = set()

        for response in self.responses:
            for format in response.formats:
                response_formats.add(format)

        return response_formats

    @staticmethod
    def get_request_body(path_dict):
        request_body_dict = path_dict.get('requestBody')
        if request_body_dict is None:
            return None

        return RequestBody(request_body_dict)

    def get_parameters_in(self):
        if self.parameters is None:
            return set()

        parameters_in = set()
        for parameter in self.parameters:
            parameters_in.add(parameter._in)

        return parameters_in

    @staticmethod
    def get_parameters(path_dict):
        params_list = path_dict.get('parameters')
        if params_list is None:
            return None

        parameters = []
        for param_dict in params_list:
            parameters.append(Parameter(param_dict))

        return parameters

    @staticmethod
    def get_responses(path_dict):
        resp_dict = path_dict.get('responses')

        responses = {}
        for code, response_dict in resp_dict.items():
            responses[code] = Response(code, response_dict)

        return responses

    @staticmethod
    def merge_dicts(fallback_dict, priority_dict):
        dikt = {}

        for key, value in fallback_dict.items():
            if key.match(ext_regex):
                dikt[key] = value

        for key, value in priority_dict.items():
            dikt[key] = value

        fallback_keys = ['summary', 'description', 'servers']
        for key in fallback_keys:
            if key not in dikt:
                dikt[key] = fallback_dict.get(key)

        fallback_parameters = fallback_dict.get('parameters')
        priority_parameters = dikt.get('parameters')

        if priority_parameters is None:
            dikt['parameters'] = fallback_parameters

        if priority_parameters is not None and fallback_parameters is not None:
            unique_parameters = set()
            for item in priority_parameters:
                priority_parameter_dict = get_reference(item)
                unique_parameters.add((priority_parameter_dict['name'], priority_parameter_dict['in']))

            for item in fallback_parameters:
                fallback_parameter_dict = get_reference(item)
                key = (fallback_parameter_dict['name'], fallback_parameter_dict['in'])
                if key not in unique_parameters:
                    dikt['parameters'].append(fallback_parameter_dict)

        return dikt


class Content(OpenAPI3):
    def __init__(self, format, content_dict):
        self.format = format
        self.type = get_schema_type(content_dict)

        self.example = content_dict.get('example')
        self.examples = content_dict.get('examples')
        self.encoding = content_dict.get('encoding')  # TODO
        self.extensions = get_extensions(content_dict)


class RequestBody(OpenAPI3):
    def __init__(self, dikt):
        request_body_dict = get_reference(dikt)

        self.formats = get_content_formats(request_body_dict)
        self.types = get_content_types(request_body_dict)
        self.contents = get_contents(request_body_dict)

        self.required = to_boolean(request_body_dict.get('required'))
        self.description = request_body_dict.get('description')
        self.extensions = get_extensions(request_body_dict)


class Response(OpenAPI3):
    """
    we don't provide any relation between format and schema. This hasn't been an issue yet
    """

    def __init__(self, response_code, dikt):
        response_dict = get_reference(dikt)

        self.code = response_code
        self.formats = get_content_formats(response_dict)
        self.types = get_content_types(response_dict)
        self.contents = get_contents(response_dict)

        self.description = response_dict.get('description')  # REQUIRED
        self.headers = response_dict.get('headers')  # TODO
        self.extensions = get_extensions(response_dict)


class Parameter(OpenAPI3):
    def __init__(self, dikt):
        parameter_dict = get_reference(dikt)

        self.name = parameter_dict.get('name')  # REQUIRED
        self._in = parameter_dict.get('in')  # REQUIRED
        self.required = to_boolean(parameter_dict.get('required'))
        self.type = get_schema_type(parameter_dict)

        self.description = parameter_dict.get('description')
        self.style = parameter_dict.get('style')  # TODO
        self.example = parameter_dict.get('example')
        self.examples = parameter_dict.get('examples')
        self.deprecated = to_boolean(parameter_dict.get('deprecated'))
        self.allowEmptyValue = to_boolean(parameter_dict.get('allowEmptyValue'))
        self.explode = to_boolean(parameter_dict.get('explode'))
        self.allowReserved = to_boolean(parameter_dict.get('allowReserved'))
        self.extensions = get_extensions(parameter_dict)
