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
    def get_content_types(dikt):
        if 'content' not in dikt:
            return None

        types = []
        for _, info in dikt.items():
            if 'schema' in info:
                types.append(get_schema_type(info['schema']))

        if len(types) == 0:
            return None

        return types

    @staticmethod
    def get_schema_type(schema_dict, depth=0):
        if (schema_dict.get('$ref')):
            s = ref.split('/')[3]
            for _ in range(depth):
                s += '>'
            return s

        if schema_dict.get('type') == 'array':
            return 'array<' + get_schema_type(schema_dict['items'], depth + 1)

        # TODO OBJECTS
        # TODO FORMAT

        s = schema_dict['type']

        for _ in range(depth):
            s += '>'

        return s

    @staticmethod
    def get_content_formats(dikt):
        if 'content' not in dikt:
            return None

        formats = []
        for format, info in dikt.items():
            formats.append(format)

        if len(formats) == 0:
            return None

        return formats

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

    def __init__(self, parent_dict, operation_dict):
        path_dict = merge_dicts(parent_dict, operation_dict)
        self.tag =
        self.method =
        self.function_name = path_dict.get('operationId')
        # self.200_response_schema =
        self.response_formats = get_response_formats(path_dict)
        self.request_body_format = get_request_body_format(path_dict)
        self.dependencies =  # TODO
        self.parameters_in = get_parameters_in(path_dict)
        self.parameters = get_parameters(path_dict)
        self.responses = get_responses(path_dict)

        self.summary = path_dict.get('summary')
        self.description = path_dict.get('description')
        self.externalDocs = path_dict.get('externalDocs')  # TODO
        self.callbacks = path_dict.get('callbacks')  # TODO
        self.security = path_dict.get('security')  # TODO
        self.servers = path_dict.get('servers')  # TODO
        self.deprecated = to_boolean(path_dict.get('deprecated'))
        self.extensions = get_extensions(path_dict)

    @staticmethod
    def get_response_formats(path_dict):
        pass

    @staticmethod
    def get_request_body_format(path_dict):
        pass

    @staticmethod
    def get_parameters_in(path_dict):
        pass

    @staticmethod
    def get_parameters(path_dict):
        pass

    @staticmethod
    def get_responses(path_dict):
        pass

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
                    unique_parameters.add(key)

        return dikt


class Response(OpenAPI3):
    """
    we don't provide any relation between format and schema. This hasn't been an issue yet
    """

    def __init__(self, response_code, dikt):
        response_dict = get_reference(dikt)

        self.code = response_code
        self.formats = get_content_formats(response_dict)
        self.schemas = get_content_types(response_dict)

        self.description = response_dict.get('description')  # REQUIRED
        self.headers = response_dict.get('headers')
        self.extensions = get_extensions(response_dict)


class Parameter(OpenAPI3):
    def __init__(self, dikt):
        parameter_dict = get_reference(dikt)

        self.name = parameter_dict.get('name')  # REQUIRED
        self._in = parameter_dict.get('in')  # REQUIRED
        self.required = to_boolean(parameter_dict.get('required'))
        self.type = get_schema_type(parameter_dict['schema'])

        self.description = parameter_dict.get('description')
        self.style = parameter_dict.get('style')
        self.example = parameter_dict.get('example')
        self.examples = parameter_dict.get('examples')
        self.deprecated = to_boolean(parameter_dict.get('deprecated'))
        self.allowEmptyValue = to_boolean(parameter_dict.get('allowEmptyValue'))
        self.explode = to_boolean(parameter_dict.get('explode'))
        self.allowReserved = to_boolean(parameter_dict.get('allowReserved'))
        self.extensions = get_extensions(parameter_dict)
