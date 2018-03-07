"""
Module that we'll import into the templates, so they can use the functions
"""

type_mapping = {
    'integer': 'int',
    'long': 'int',
    'float': 'float',
    'double': 'float',
    'string': 'str',
    'byte': 'str',
    'binary': 'str',
    'boolean': 'bool',
    'date': 'str',
    'dateTime': 'str',
    'password': 'str',
}
