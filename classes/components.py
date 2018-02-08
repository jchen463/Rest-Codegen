"""
We'll have to figure out how each of these are handled during code generation
Dependency mapping is important, because inside each of their dictionaries, they can contain references to other class instances
Unsure if these classes will be needed, but if anything should be in a class it should be these, because they're referenced everywhere in the spec
"""


class Schema:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt

    def schema_method():
        pass


class Response:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt

    def response_method():
        pass


class Parameter:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt


class Example:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt


class RequestBody:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt


class Header:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt


class SecurityScheme:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt


class Link:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt


class Callback:
    def __init__(self, name, dikt):
        self.name = name
        self.dikt = dikt
