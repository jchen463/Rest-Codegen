class Rep:
    def __repr__(self):
        return repr(vars(self))

# class Rep(object):
#     """A mixin implementing a simple __repr__."""
#     def __repr__(self):
#         return "<{klass} @{id:x} {attrs}>".format(
#             klass=self.__class__.__name__,
#             id=id(self) & 0xFFFFFF,
#             attrs=" ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
#             )