# collections: Counter, defaultdict, OrderedDict, deque, namedtuple, ChainMap.
#
# Author: Alexius Academia
# Date: 2026-10-08
#
# PyTessel's classes can't inherit from dict or tuple, so these are
# classes of their own that hold a dict (or a list, or a tuple) and do
# what one does: indexing, len(), `in`, iteration, ==, the methods. What
# they can't be is a dict or a tuple to isinstance().


def _is_mapping(x):
    return isinstance(x, (dict, _DictLike, ChainMap))


def _plain(x):
    # The dict inside one of this module's dictionaries.
    if isinstance(x, _DictLike):
        return x._d
    return x


class _DictLike:
    """What Counter, defaultdict and OrderedDict share: a dict, in `_d`."""

    def __len__(self):
        return len(self._d)

    def __iter__(self):
        return iter(self._d)

    def __contains__(self, key):
        return key in self._d

    def __getitem__(self, key):
        return self._d[key]

    def __setitem__(self, key, value):
        self._d[key] = value

    def __delitem__(self, key):
        del self._d[key]

    def __eq__(self, other):
        if not _is_mapping(other):
            return False
        return self._d == _plain(other)

    def __ne__(self, other):
        return not self == other

    def __or__(self, other):
        if not _is_mapping(other):
            raise TypeError("unsupported operand type(s) for |: '%s' and '%s'" % (type(self).__name__, type(other).__name__))
        result = self.copy()
        result.update(other)
        return result

    def __ior__(self, other):
        self.update(other)
        return self

    def keys(self):
        return self._d.keys()

    def values(self):
        return self._d.values()

    def items(self):
        return self._d.items()

    def get(self, key, default=None):
        return self._d.get(key, default)

    def pop(self, key, *default):
        return self._d.pop(key, *default)

    def popitem(self):
        return self._d.popitem()

    def setdefault(self, key, default=None):
        return self._d.setdefault(key, default)

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 argument, got %d" % len(args))
        for other in args:
            self._d.update(_plain(other))
        if kwargs:
            self._d.update(kwargs)

    def clear(self):
        self._d.clear()

    def __copy__(self):
        return self.copy()


# ---- Counter ----

def _by_count(item):
    return item[1]


class Counter(_DictLike):
    """Counts things: Counter("hello")["l"] is 2, and a missing key counts 0."""

    def __init__(self, iterable=None, **kwds):
        self._d = {}
        self.update(iterable, **kwds)

    def __getitem__(self, key):
        return self._d.get(key, 0)

    def __delitem__(self, key):
        # (Unlike a dict's: nothing happens when the key isn't there.)
        if key in self._d:
            del self._d[key]

    def __repr__(self):
        if not self._d:
            return "Counter()"
        return "Counter({%s})" % ", ".join(["%r: %r" % pair for pair in self.most_common()])

    def total(self):
        """The sum of the counts."""
        return sum(self._d.values())

    def most_common(self, n=None):
        """The n most common things and their counts, most common first."""
        ordered = sorted(self._d.items(), key=_by_count, reverse=True)
        if n is None:
            return ordered
        return ordered[:n] if n > 0 else []

    def elements(self):
        """Each thing as many times as its count."""
        for element in self._d:
            for i in range(self._d[element]):
                yield element

    def update(self, iterable=None, **kwds):
        """Adds counts: of the things of an iterable, or from another mapping."""
        d = self._d
        if iterable is not None:
            if _is_mapping(iterable):
                for element in iterable:
                    d[element] = d.get(element, 0) + iterable[element]
            else:
                for element in iterable:
                    d[element] = d.get(element, 0) + 1
        for element in kwds:
            d[element] = d.get(element, 0) + kwds[element]

    def subtract(self, iterable=None, **kwds):
        """Takes counts away (they can go below zero)."""
        d = self._d
        if iterable is not None:
            if _is_mapping(iterable):
                for element in iterable:
                    d[element] = d.get(element, 0) - iterable[element]
            else:
                for element in iterable:
                    d[element] = d.get(element, 0) - 1
        for element in kwds:
            d[element] = d.get(element, 0) - kwds[element]

    def copy(self):
        return Counter(self)

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError("Counter.fromkeys() is undefined.  Use Counter(iterable) instead.")

    def _other(self, other, symbol):
        if not isinstance(other, Counter):
            raise TypeError("unsupported operand type(s) for %s: 'Counter' and '%s'" % (symbol, type(other).__name__))

    def __add__(self, other):
        self._other(other, "+")
        result = Counter()
        for element in self._d:
            count = self._d[element] + other[element]
            if count > 0:
                result[element] = count
        for element in other._d:
            if element not in self._d and other._d[element] > 0:
                result[element] = other._d[element]
        return result

    def __sub__(self, other):
        self._other(other, "-")
        result = Counter()
        for element in self._d:
            count = self._d[element] - other[element]
            if count > 0:
                result[element] = count
        for element in other._d:
            if element not in self._d and other._d[element] < 0:
                result[element] = 0 - other._d[element]
        return result

    def __or__(self, other):
        self._other(other, "|")
        result = Counter()
        for element in self._d:
            count = self._d[element]
            theirs = other[element]
            if theirs > count:
                count = theirs
            if count > 0:
                result[element] = count
        for element in other._d:
            if element not in self._d and other._d[element] > 0:
                result[element] = other._d[element]
        return result

    def __and__(self, other):
        self._other(other, "&")
        result = Counter()
        for element in self._d:
            count = self._d[element]
            theirs = other[element]
            if theirs < count:
                count = theirs
            if count > 0:
                result[element] = count
        return result

    def __pos__(self):
        result = Counter()
        for element in self._d:
            if self._d[element] > 0:
                result[element] = self._d[element]
        return result

    def __neg__(self):
        result = Counter()
        for element in self._d:
            if self._d[element] < 0:
                result[element] = 0 - self._d[element]
        return result

    def _keep_positive(self):
        for element in list(self._d):
            if not self._d[element] > 0:
                del self._d[element]
        return self

    def __iadd__(self, other):
        self._other(other, "+=")
        for element in other._d:
            self._d[element] = self._d.get(element, 0) + other._d[element]
        return self._keep_positive()

    def __isub__(self, other):
        self._other(other, "-=")
        for element in other._d:
            self._d[element] = self._d.get(element, 0) - other._d[element]
        return self._keep_positive()

    def __ior__(self, other):
        self._other(other, "|=")
        for element in other._d:
            if other._d[element] > self._d.get(element, 0):
                self._d[element] = other._d[element]
        return self._keep_positive()

    def __iand__(self, other):
        self._other(other, "&=")
        for element in list(self._d):
            if other[element] < self._d[element]:
                self._d[element] = other[element]
        return self._keep_positive()


# ---- defaultdict ----

class defaultdict(_DictLike):
    """A dict that makes a value, with default_factory(), for a key it hasn't got."""

    def __init__(self, default_factory=None, *args, **kwargs):
        if default_factory is not None and not callable(default_factory):
            raise TypeError("first argument must be callable or None")
        self.default_factory = default_factory
        self._d = {}
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        d = self._d
        if key in d:
            return d[key]
        return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        value = self.default_factory()
        self._d[key] = value
        return value

    def __repr__(self):
        return "defaultdict(%r, %r)" % (self.default_factory, self._d)

    def copy(self):
        return defaultdict(self.default_factory, self._d)


# ---- OrderedDict ----

class OrderedDict(_DictLike):
    """A dict that can move its keys about: move_to_end(), popitem(last=False)."""

    def __init__(self, *args, **kwargs):
        self._d = {}
        self.update(*args, **kwargs)

    def __repr__(self):
        if not self._d:
            return "OrderedDict()"
        return "OrderedDict(%r)" % (list(self._d.items()),)

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            # (Two of them are equal when their order is the same too.)
            return list(self._d.items()) == list(other._d.items())
        if not _is_mapping(other):
            return False
        return self._d == _plain(other)

    def __reversed__(self):
        return reversed(list(self._d))

    def move_to_end(self, key, last=True):
        """Moves a key to the end (or to the start, with last=False)."""
        if key not in self._d:
            raise KeyError(key)
        value = self._d.pop(key)
        if last:
            self._d[key] = value
        else:
            old = self._d
            self._d = {key: value}
            self._d.update(old)

    def popitem(self, last=True):
        """Removes and gives the last (key, value), or the first with last=False."""
        if not self._d:
            raise KeyError("dictionary is empty")
        if last:
            return self._d.popitem()
        for key in self._d:
            break
        return (key, self._d.pop(key))

    def copy(self):
        return OrderedDict(self._d)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        result = cls()
        for key in iterable:
            result[key] = value
        return result


# ---- deque ----

class deque:
    """A list that's quick to add to and take from at both ends."""

    def __init__(self, iterable=(), maxlen=None):
        if maxlen is not None:
            if not isinstance(maxlen, int):
                raise TypeError("an integer is required")
            if maxlen < 0:
                raise ValueError("maxlen must be non-negative")
        self.maxlen = maxlen
        # The items are _items[_head:]: taking one from the left only
        # moves _head (and the list is cut down now and then).
        self._items = []
        self._head = 0
        self.extend(iterable)

    def _pack(self):
        if self._head:
            self._items = self._items[self._head:]
            self._head = 0
        return self._items

    def __len__(self):
        return len(self._items) - self._head

    def __bool__(self):
        return len(self._items) > self._head

    def __iter__(self):
        return iter(self._pack()[:])

    def __reversed__(self):
        return reversed(self._pack()[:])

    def __contains__(self, value):
        return value in self._pack()

    def __repr__(self):
        if self.maxlen is None:
            return "deque(%r)" % (self._pack(),)
        return "deque(%r, maxlen=%d)" % (self._pack(), self.maxlen)

    def __eq__(self, other):
        return isinstance(other, deque) and self._pack() == other._pack()

    def __ne__(self, other):
        return not self == other

    def _compare(self, other, symbol):
        if not isinstance(other, deque):
            raise TypeError("'%s' not supported between instances of 'collections.deque' and '%s'" % (symbol, type(other).__name__))
        return other._pack()

    def __lt__(self, other):
        return self._pack() < self._compare(other, "<")

    def __le__(self, other):
        return self._pack() <= self._compare(other, "<=")

    def __gt__(self, other):
        return self._pack() > self._compare(other, ">")

    def __ge__(self, other):
        return self._pack() >= self._compare(other, ">=")

    def _place(self, index):
        size = len(self._items) - self._head
        if not isinstance(index, int):
            raise TypeError("sequence index must be integer, not '%s'" % type(index).__name__)
        if index < 0:
            index += size
        if index < 0 or index >= size:
            raise IndexError("deque index out of range")
        return self._head + index

    def __getitem__(self, index):
        return self._items[self._place(index)]

    def __setitem__(self, index, value):
        self._items[self._place(index)] = value

    def __delitem__(self, index):
        at = self._place(index)
        del self._items[at]

    def __add__(self, other):
        if not isinstance(other, deque):
            raise TypeError("can only concatenate deque (not \"%s\") to deque" % type(other).__name__)
        result = deque(self, self.maxlen)
        result.extend(other)
        return result

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __mul__(self, n):
        return deque(self._pack() * n, self.maxlen)

    def __rmul__(self, n):
        return deque(self._pack() * n, self.maxlen)

    def __copy__(self):
        return deque(self, self.maxlen)

    def append(self, x):
        """Adds x on the right."""
        if self.maxlen is not None and len(self._items) - self._head >= self.maxlen:
            if self.maxlen == 0:
                return
            self.popleft()
        self._items.append(x)

    def appendleft(self, x):
        """Adds x on the left."""
        if self.maxlen is not None and len(self._items) - self._head >= self.maxlen:
            if self.maxlen == 0:
                return
            self._items.pop()
        if self._head > 0:
            self._head -= 1
            self._items[self._head] = x
        else:
            self._items.insert(0, x)

    def pop(self):
        """Removes and gives the item on the right."""
        if len(self._items) <= self._head:
            raise IndexError("pop from an empty deque")
        return self._items.pop()

    def popleft(self):
        """Removes and gives the item on the left."""
        head = self._head
        items = self._items
        if len(items) <= head:
            raise IndexError("pop from an empty deque")
        x = items[head]
        items[head] = None
        head += 1
        if head > 32 and head * 2 > len(items):
            self._items = items[head:]
            head = 0
        self._head = head
        return x

    def extend(self, iterable):
        """Adds each item on the right."""
        if iterable is self:
            iterable = list(iterable)
        if self.maxlen is None:
            self._items.extend(iterable)
        else:
            for x in iterable:
                self.append(x)

    def extendleft(self, iterable):
        """Adds each item on the left (so they end up in the opposite order)."""
        if iterable is self:
            iterable = list(iterable)
        for x in iterable:
            self.appendleft(x)

    def clear(self):
        self._items = []
        self._head = 0

    def copy(self):
        return deque(self, self.maxlen)

    def count(self, x):
        return self._pack().count(x)

    def index(self, x, start=0, stop=None):
        items = self._pack()
        size = len(items)
        if start < 0:
            start = max(start + size, 0)
        if stop is None or stop > size:
            stop = size
        elif stop < 0:
            stop = max(stop + size, 0)
        for i in range(start, stop):
            if items[i] == x:
                return i
        raise ValueError("%r is not in deque" % (x,))

    def insert(self, i, x):
        if self.maxlen is not None and len(self) >= self.maxlen:
            raise IndexError("deque already at its maximum size")
        self._pack().insert(i, x)

    def remove(self, value):
        items = self._pack()
        for i in range(len(items)):
            if items[i] == value:
                del items[i]
                return
        raise ValueError("deque.remove(x): x not in deque")

    def reverse(self):
        self._pack().reverse()

    def rotate(self, n=1):
        """Moves the items n steps to the right (to the left, for a negative n)."""
        items = self._pack()
        size = len(items)
        if size == 0:
            return
        k = n % size
        if k:
            self._items = items[size - k:] + items[:size - k]


# ---- namedtuple ----

_KEYWORDS = ("False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue",
             "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in",
             "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield")


def _quoted_names(names):
    # 'a', 'b' and 'c'
    quoted = ["'%s'" % name for name in names]
    if len(quoted) == 1:
        return quoted[0]
    if len(quoted) == 2:
        return quoted[0] + " and " + quoted[1]
    return ", ".join(quoted[:len(quoted) - 1]) + ", and " + quoted[len(quoted) - 1]


def _field_getter(index):
    def getter(self):
        return self._values[index]
    return getter


class _NamedTuple:
    """What every class namedtuple() makes inherits: a tuple, in `_values`."""

    def __init__(self, *args, **kwargs):
        fields = self._fields
        count = len(fields)
        if len(args) > count:
            raise TypeError("%s.__new__() takes %d positional argument%s but %d were given"
                            % (type(self).__name__, count + 1, "" if count == 0 else "s", len(args) + 1))
        values = list(args)
        missing = []
        defaults = self._field_defaults
        for i in range(len(args), count):
            name = fields[i]
            if name in kwargs:
                values.append(kwargs.pop(name))
            elif name in defaults:
                values.append(defaults[name])
            else:
                missing.append(name)
        for name in kwargs:
            if name in fields:
                raise TypeError("%s.__new__() got multiple values for argument '%s'" % (type(self).__name__, name))
            raise TypeError("%s.__new__() got an unexpected keyword argument '%s'" % (type(self).__name__, name))
        if missing:
            raise TypeError("%s.__new__() missing %d required positional argument%s: %s"
                            % (type(self).__name__, len(missing), "" if len(missing) == 1 else "s",
                               _quoted_names(missing)))
        self._values = tuple(values)

    def __repr__(self):
        parts = []
        for i in range(len(self._fields)):
            parts.append("%s=%r" % (self._fields[i], self._values[i]))
        return "%s(%s)" % (type(self).__name__, ", ".join(parts))

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def __getitem__(self, index):
        return self._values[index]

    def __contains__(self, value):
        return value in self._values

    def __hash__(self):
        return hash(self._values)

    def __eq__(self, other):
        if isinstance(other, _NamedTuple):
            return self._values == other._values
        return isinstance(other, tuple) and self._values == other

    def __ne__(self, other):
        return not self == other

    def _tuple_of(self, other, symbol):
        if isinstance(other, _NamedTuple):
            return other._values
        if isinstance(other, tuple):
            return other
        raise TypeError("'%s' not supported between instances of '%s' and '%s'"
                        % (symbol, type(self).__name__, type(other).__name__))

    def __lt__(self, other):
        return self._values < self._tuple_of(other, "<")

    def __le__(self, other):
        return self._values <= self._tuple_of(other, "<=")

    def __gt__(self, other):
        return self._values > self._tuple_of(other, ">")

    def __ge__(self, other):
        return self._values >= self._tuple_of(other, ">=")

    def __add__(self, other):
        if isinstance(other, _NamedTuple):
            return self._values + other._values
        return self._values + other

    def __radd__(self, other):
        return other + self._values

    def __mul__(self, n):
        return self._values * n

    def __rmul__(self, n):
        return self._values * n

    def count(self, value):
        return self._values.count(value)

    def index(self, value):
        return self._values.index(value)

    def _asdict(self):
        """The fields and their values, as a dict."""
        out = {}
        for i in range(len(self._fields)):
            out[self._fields[i]] = self._values[i]
        return out

    def _replace(self, **kwargs):
        """A copy, with some fields given new values."""
        values = []
        for name in self._fields:
            if name in kwargs:
                values.append(kwargs.pop(name))
            else:
                values.append(getattr(self, name))
        if kwargs:
            raise ValueError("Got unexpected field names: %r" % (list(kwargs),))
        return type(self)(*values)

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        import copy
        return type(self)(*[copy.deepcopy(v, memo) for v in self._values])


def _nt_make(cls, iterable):
    values = tuple(iterable)
    if len(values) != len(cls._fields):
        raise TypeError("Expected %d arguments, got %d" % (len(cls._fields), len(values)))
    return cls(*values)


def _nt_class(typename):
    # The class is written out and run, so that it has the name asked
    # for. (It's the only class among this function's variables.)
    exec("class %s(_NamedTuple):\n    pass\n" % typename)
    for value in locals().values():
        if isinstance(value, type):
            return value


def namedtuple(typename, field_names, rename=False, defaults=None, module=None):
    """A new class like a tuple, whose items also have names: Point = namedtuple("Point", "x y")."""
    if isinstance(field_names, str):
        field_names = field_names.replace(",", " ").split()
    field_names = [str(name) for name in field_names]
    typename = str(typename)
    if rename:
        seen = set()
        for index in range(len(field_names)):
            name = field_names[index]
            if not name.isidentifier() or name in _KEYWORDS or name.startswith("_") or name in seen:
                field_names[index] = "_%d" % index
            seen.add(name)
    for name in [typename] + field_names:
        if not name.isidentifier():
            raise ValueError("Type names and field names must be valid identifiers: %r" % name)
        if name in _KEYWORDS:
            raise ValueError("Type names and field names cannot be a keyword: %r" % name)
    seen = set()
    for name in field_names:
        if name.startswith("_") and not rename:
            raise ValueError("Field names cannot start with an underscore: %r" % name)
        if name in seen:
            raise ValueError("Encountered duplicate field name: %r" % name)
        seen.add(name)
    field_defaults = {}
    if defaults is not None:
        defaults = tuple(defaults)
        if len(defaults) > len(field_names):
            raise TypeError("Got more default values than field names")
        first = len(field_names) - len(defaults)
        for i in range(len(defaults)):
            field_defaults[field_names[first + i]] = defaults[i]
    cls = _nt_class(typename)
    cls._fields = tuple(field_names)
    cls._field_defaults = field_defaults
    cls._make = classmethod(_nt_make)
    for index in range(len(field_names)):
        setattr(cls, field_names[index], property(_field_getter(index)))
    return cls


# ---- ChainMap ----

class ChainMap:
    """Several mappings seen as one: a key is looked for in each in turn."""

    def __init__(self, *maps):
        self.maps = list(maps) or [{}]

    def __getitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                return mapping[key]
        raise KeyError(key)

    def get(self, key, default=None):
        for mapping in self.maps:
            if key in mapping:
                return mapping[key]
        return default

    def _merged(self):
        merged = {}
        for mapping in reversed(self.maps):
            for key in mapping:
                merged[key] = None
        return merged

    def __len__(self):
        return len(self._merged())

    def __iter__(self):
        return iter(self._merged())

    def __contains__(self, key):
        for mapping in self.maps:
            if key in mapping:
                return True
        return False

    def __bool__(self):
        for mapping in self.maps:
            if mapping:
                return True
        return False

    def __repr__(self):
        return "ChainMap(%s)" % ", ".join([repr(m) for m in self.maps])

    def __eq__(self, other):
        if isinstance(other, ChainMap):
            return dict(self.items()) == dict(other.items())
        if not _is_mapping(other):
            return False
        return dict(self.items()) == _plain(other)

    def keys(self):
        return list(self._merged())

    def values(self):
        return [self[key] for key in self._merged()]

    def items(self):
        return [(key, self[key]) for key in self._merged()]

    def copy(self):
        return ChainMap(self.maps[0].copy(), *self.maps[1:])

    def new_child(self, m=None):
        """A new ChainMap with a new mapping in front of this one's."""
        if m is None:
            m = {}
        return ChainMap(m, *self.maps)

    @property
    def parents(self):
        """A ChainMap of every mapping but the first."""
        return ChainMap(*self.maps[1:])

    def __setitem__(self, key, value):
        self.maps[0][key] = value

    def __delitem__(self, key):
        if key not in self.maps[0]:
            raise KeyError("Key not found in the first mapping: %r" % (key,))
        del self.maps[0][key]

    def popitem(self):
        if not self.maps[0]:
            raise KeyError("No keys found in the first mapping.")
        return self.maps[0].popitem()

    def pop(self, key, *args):
        if key not in self.maps[0]:
            if args:
                return args[0]
            raise KeyError("Key not found in the first mapping: %r" % (key,))
        return self.maps[0].pop(key)

    def clear(self):
        self.maps[0].clear()

    def update(self, *args, **kwargs):
        self.maps[0].update(*args, **kwargs)

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        self[key] = default
        return default
