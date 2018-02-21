import re
from .keyword_map import keyword_to_object

ext_regex = re.compile('x-.*')


def parse_dict(dikt, allowed, required=[], objects=[], mappings=[], booleans=[], arrays=[]):
    d = {}
    for attr in required:
        if attr not in dikt:
            raise ValueError('required field ' + attr + ' is missing')
    for attr in allowed:
        d[attr] = None

    d['extensions'] = []

    for key, value in dikt.items():
        if key in objects:
            d[key] = get_object(key, value)
        elif key in mappings:
            d[key] = get_mapping(key, value)
        elif key in arrays:  # server: [<Server Object>]
            d[key] = get_array(key, value)
        elif key in booleans:
            d[key] = get_boolean(value)
        elif ext_regex.match(key):
            d['extensions'].append({key: value})
        else:  # string
            d[key] = value

    for key, value in list(d.items()):
        if key not in allowed:
            del d[key]

    return d


def get_mapping(keyword, dikt):
    mapping = {}

    for key, value in dikt.items():
        mapping[key] = get_object(keyword, value)

    return mapping


def get_array(keyword, arr):
    array = []

    for dikt in arr:
        array.append(get_object(keyword, dikt))

    return array


def get_boolean(value):
    if type(value) == bool:
        return value
    if type(value) == str and value.lower() == 'true':
        return True
    if type(value) == str and value.lower() == 'false':
        return False
    return None


def get_object(keyword, dikt):
    if '$ref' in dikt:
        from .reference import Reference
        return Reference(dikt)
    if keyword in keyword_to_object:
        return keyword_to_object[keyword](dikt)
    return None
