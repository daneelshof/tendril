class Monostate(object):
    """A more Pythonic alternative to Singleton"""
    __state = {}

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self.__dict__ = cls.__state
        return self
