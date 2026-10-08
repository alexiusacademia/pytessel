"""enum: Enum, IntEnum, Flag, auto and unique.

A member is an object of its enum class with a `name` and a `value`; the
metaclass makes one for each plain attribute of the class body, in the
order they're written. An IntEnum's members aren't ints here (PyTessel has
no classes that inherit from int): they compare, hash and do arithmetic
as their values.
"""

__all__ = ["Enum", "IntEnum", "Flag", "IntFlag", "EnumMeta", "EnumType", "auto", "unique"]


class auto:
    """A value to be chosen: one more than the member before."""

    __module__ = "enum"


def _is_member_value(key, value):
    if key.startswith("_"):
        return False
    if callable(value):
        return False
    return type(value).__name__ not in ("property", "staticmethod", "classmethod", "function")


class EnumType(type):
    __module__ = "enum"

    def __new__(mcs, name, bases, namespace):
        plain = {}
        found = []
        for key, value in namespace.items():
            if _is_member_value(key, value):
                found.append((key, value))
            else:
                plain[key] = value
        cls = super().__new__(mcs, name, bases, plain)
        members = {}
        by_value = []
        inherited = getattr(cls, "_member_map_", None)
        if inherited and found:
            raise TypeError("%r cannot extend %r" % (cls, bases[0]))
        cls._member_map_ = members
        cls._by_value_ = by_value
        cls._member_names_ = []
        last = []
        for key, value in found:
            if isinstance(value, auto):
                value = cls._generate_next_value_(key, 1, len(cls._member_names_), last)
            last.append(value)
            member = None
            for seen_value, seen in by_value:
                if seen_value == value and type(seen_value) is type(value):
                    member = seen
            if member is None:
                member = object.__new__(cls)
                member._name_ = key
                member._value_ = value
                by_value.append((value, member))
                cls._member_names_.append(key)
            members[key] = member
            type.__setattr__(cls, key, member)
        return cls

    def __call__(cls, value):
        for seen_value, member in cls._by_value_:
            if seen_value == value:
                return member
        missing = cls._missing_(value)
        if missing is not None:
            return missing
        raise ValueError("%r is not a valid %s" % (value, cls.__name__))

    def __iter__(cls):
        return iter([cls._member_map_[name] for name in cls._member_names_])

    def __reversed__(cls):
        return iter([cls._member_map_[name] for name in reversed(cls._member_names_)])

    def __len__(cls):
        return len(cls._member_names_)

    def __getitem__(cls, name):
        return cls._member_map_[name]

    def __contains__(cls, item):
        if isinstance(item, cls):
            return True
        for seen_value, member in cls._by_value_:
            if seen_value == item:
                return True
        return False

    def __repr__(cls):
        return "<enum %r>" % cls.__name__

    def __setattr__(cls, name, value):
        if name in cls.__dict__.get("_member_map_", {}):
            raise AttributeError("cannot reassign member %r" % name)
        type.__setattr__(cls, name, value)

    @property
    def __members__(cls):
        return dict(cls._member_map_)


EnumMeta = EnumType


class Enum(metaclass=EnumType):
    __module__ = "enum"

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        for value in reversed(last_values):
            if isinstance(value, int):
                return value + 1
        return start

    @classmethod
    def _missing_(cls, value):
        return None

    @property
    def name(self):
        return self._name_

    @property
    def value(self):
        return self._value_

    def __repr__(self):
        return "<%s.%s: %r>" % (type(self).__name__, self._name_, self._value_)

    def __str__(self):
        return "%s.%s" % (type(self).__name__, self._name_)

    def __hash__(self):
        return hash(self._name_)

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    def __reduce__(self):
        return (type(self), (self._value_,))


class IntEnum(Enum):
    __module__ = "enum"

    def __str__(self):
        return str(self._value_)

    def __format__(self, spec):
        return format(self._value_, spec)

    def __int__(self):
        return self._value_

    def __index__(self):
        return self._value_

    def __float__(self):
        return float(self._value_)

    def __hash__(self):
        return hash(self._value_)

    def __bool__(self):
        return bool(self._value_)

    def __eq__(self, other):
        return self._value_ == _plain(other)

    def __ne__(self, other):
        return self._value_ != _plain(other)

    def __lt__(self, other):
        return self._value_ < _plain(other)

    def __le__(self, other):
        return self._value_ <= _plain(other)

    def __gt__(self, other):
        return self._value_ > _plain(other)

    def __ge__(self, other):
        return self._value_ >= _plain(other)

    def __add__(self, other):
        return self._value_ + _plain(other)

    def __radd__(self, other):
        return _plain(other) + self._value_

    def __sub__(self, other):
        return self._value_ - _plain(other)

    def __rsub__(self, other):
        return _plain(other) - self._value_

    def __mul__(self, other):
        return self._value_ * _plain(other)

    def __rmul__(self, other):
        return _plain(other) * self._value_

    def __floordiv__(self, other):
        return self._value_ // _plain(other)

    def __truediv__(self, other):
        return self._value_ / _plain(other)

    def __mod__(self, other):
        return self._value_ % _plain(other)

    def __neg__(self):
        return -self._value_


def _plain(value):
    if isinstance(value, Enum):
        return value._value_
    return value


class Flag(Enum):
    """Members are bits: they combine with | and are tested with & and `in`."""

    __module__ = "enum"

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        if not last_values:
            return 1
        high = max(last_values)
        bit = 1
        while bit <= high:
            bit *= 2
        return bit

    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, int) or value < 0:
            return None
        known = 0
        for seen_value, member in cls._by_value_:
            known |= seen_value
        if value & ~known:
            return None
        combined = object.__new__(cls)
        names = [member._name_ for seen_value, member in cls._by_value_ if seen_value and seen_value & value == seen_value
                 and seen_value & (seen_value - 1) == 0]
        combined._name_ = "|".join(names) if names else None
        combined._value_ = value
        return combined

    def __or__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)(self._value_ | other._value_)

    def __and__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)(self._value_ & other._value_)

    def __xor__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)(self._value_ ^ other._value_)

    def __invert__(self):
        known = 0
        for seen_value, member in type(self)._by_value_:
            known |= seen_value
        return type(self)(known & ~self._value_)

    def __contains__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("unsupported operand type(s) for 'in': %r and %r" % (type(other).__name__, type(self).__name__))
        return other._value_ & self._value_ == other._value_

    def __bool__(self):
        return bool(self._value_)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self._value_ == other._value_

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._value_)

    def __iter__(self):
        for seen_value, member in type(self)._by_value_:
            if seen_value and seen_value & self._value_ == seen_value and seen_value & (seen_value - 1) == 0:
                yield member

    def __repr__(self):
        if self._name_ is None:
            return "<%s: %r>" % (type(self).__name__, self._value_)
        return "<%s.%s: %r>" % (type(self).__name__, self._name_, self._value_)

    def __str__(self):
        if self._name_ is None:
            return "%s(%r)" % (type(self).__name__, self._value_)
        return "%s.%s" % (type(self).__name__, self._name_)


IntFlag = Flag


def unique(enumeration):
    """A class decorator: no two names for one value."""
    duplicates = []
    for name, member in enumeration.__members__.items():
        if name != member.name:
            duplicates.append("%s -> %s" % (name, member.name))
    if duplicates:
        raise ValueError("duplicate values found in %r: %s" % (enumeration, ", ".join(duplicates)))
    return enumeration
