"""abc: abstract base classes.

A class whose metaclass is ABCMeta (or that inherits from ABC) can't be
instantiated while a method marked @abstractmethod is not filled in. The
interpreter itself keeps track of which are (objects.tsl); this module
only gives the names.
"""

abstractmethod = __abstractmethod__


class ABCMeta(type):
    __module__ = "abc"


class ABC(metaclass=ABCMeta):
    __module__ = "abc"
