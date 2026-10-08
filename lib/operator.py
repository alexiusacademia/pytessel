# operator: Python's operators as functions, and makers of small functions.
#
# Author: Alexius Academia
# Date: 2026-10-08

# (The built-in abs, before this module's own takes the name.)
_abs = abs


def lt(a, b):
    return a < b


def le(a, b):
    return a <= b


def eq(a, b):
    return a == b


def ne(a, b):
    return a != b


def ge(a, b):
    return a >= b


def gt(a, b):
    return a > b


def not_(a):
    return not a


def truth(a):
    return True if a else False


def is_(a, b):
    return a is b


def is_not(a, b):
    return a is not b


def abs(a):
    return _abs(a)


def add(a, b):
    return a + b


def and_(a, b):
    return a & b


def floordiv(a, b):
    return a // b


def index(a):
    if not isinstance(a, int):
        raise TypeError("'%s' object cannot be interpreted as an integer" % type(a).__name__)
    return a


def inv(a):
    return ~a


invert = inv


def lshift(a, b):
    return a << b


def mod(a, b):
    return a % b


def mul(a, b):
    return a * b


def neg(a):
    return -a


def or_(a, b):
    return a | b


def pos(a):
    return +a


def pow(a, b):
    return a ** b


def rshift(a, b):
    return a >> b


def sub(a, b):
    return a - b


def truediv(a, b):
    return a / b


def xor(a, b):
    return a ^ b


def concat(a, b):
    if not hasattr(a, "__getitem__") and not isinstance(a, (str, list, tuple)):
        raise TypeError("'%s' object can't be concatenated" % type(a).__name__)
    return a + b


def contains(a, b):
    return b in a


def countOf(a, b):
    count = 0
    for item in a:
        if item is b or item == b:
            count += 1
    return count


def delitem(a, b):
    del a[b]


def getitem(a, b):
    return a[b]


def indexOf(a, b):
    i = 0
    for item in a:
        if item is b or item == b:
            return i
        i += 1
    raise ValueError("sequence.index(x): x not in sequence")


def setitem(a, b, c):
    a[b] = c


def length_hint(obj, default=0):
    try:
        return len(obj)
    except TypeError:
        return default


class attrgetter:
    """attrgetter("a.b")(x) is x.a.b; with several names, a tuple of them."""

    __module__ = "operator"

    def __init__(self, attr, *attrs):
        names = (attr,) + attrs
        for name in names:
            if not isinstance(name, str):
                raise TypeError("attribute name must be a string")
        self._attrs = names

    def _resolve(self, obj, name):
        for part in name.split("."):
            obj = getattr(obj, part)
        return obj

    def __call__(self, obj):
        if len(self._attrs) == 1:
            return self._resolve(obj, self._attrs[0])
        return tuple([self._resolve(obj, name) for name in self._attrs])

    def __repr__(self):
        return "operator.attrgetter(%s)" % ", ".join([repr(a) for a in self._attrs])


class itemgetter:
    """itemgetter(1)(x) is x[1]; with several items, a tuple of them."""

    __module__ = "operator"

    def __init__(self, item, *items):
        self._items = (item,) + items

    def __call__(self, obj):
        if len(self._items) == 1:
            return obj[self._items[0]]
        return tuple([obj[item] for item in self._items])

    def __repr__(self):
        return "operator.itemgetter(%s)" % ", ".join([repr(i) for i in self._items])


class methodcaller:
    """methodcaller("name", 1)(x) is x.name(1)."""

    __module__ = "operator"

    def __init__(self, name, *args, **kwargs):
        if not isinstance(name, str):
            raise TypeError("method name must be a string")
        self._name = name
        self._args = args
        self._kwargs = kwargs

    def __call__(self, obj):
        return getattr(obj, self._name)(*self._args, **self._kwargs)

    def __repr__(self):
        parts = [repr(self._name)]
        for a in self._args:
            parts.append(repr(a))
        for k in self._kwargs:
            parts.append("%s=%r" % (k, self._kwargs[k]))
        return "operator.methodcaller(%s)" % ", ".join(parts)


def iadd(a, b):
    a += b
    return a


def iand(a, b):
    a &= b
    return a


def iconcat(a, b):
    a += b
    return a


def ifloordiv(a, b):
    a //= b
    return a


def ilshift(a, b):
    a <<= b
    return a


def imod(a, b):
    a %= b
    return a


def imul(a, b):
    a *= b
    return a


def ior(a, b):
    a |= b
    return a


def ipow(a, b):
    a **= b
    return a


def irshift(a, b):
    a >>= b
    return a


def isub(a, b):
    a -= b
    return a


def itruediv(a, b):
    a /= b
    return a


def ixor(a, b):
    a ^= b
    return a


__lt__ = lt
__le__ = le
__eq__ = eq
__ne__ = ne
__ge__ = ge
__gt__ = gt
__add__ = add
__sub__ = sub
__mul__ = mul
__truediv__ = truediv
__floordiv__ = floordiv
__mod__ = mod
__neg__ = neg
__not__ = not_
__getitem__ = getitem
__contains__ = contains
