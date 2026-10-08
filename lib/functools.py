# functools: functions that work on functions.
#
# Author: Alexius Academia
# Date: 2026-10-08
from _functools import reduce

WRAPPER_ASSIGNMENTS = ("__module__", "__name__", "__qualname__", "__doc__")
WRAPPER_UPDATES = ("__dict__",)


def update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """Makes a wrapper function look like the function it wraps."""
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        extra = getattr(wrapped, attr, None)
        if extra:
            for name in extra:
                if name not in assigned:
                    setattr(wrapper, name, extra[name])
    wrapper.__wrapped__ = wrapped
    return wrapper


def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """A decorator for a wrapper function: @wraps(f) gives it f's name."""
    def decorator(wrapper):
        return update_wrapper(wrapper, wrapped, assigned, updated)
    return decorator


class partial:
    """A function with some of its arguments already given."""

    def __init__(self, *args, **keywords):
        if not args:
            raise TypeError("type 'partial' takes at least one argument")
        func = args[0]
        args = tuple(args[1:])
        if not callable(func):
            raise TypeError("the first argument must be callable")
        if isinstance(func, partial):
            args = func.args + args
            merged = dict(func.keywords)
            merged.update(keywords)
            keywords = merged
            func = func.func
        self.func = func
        self.args = args
        self.keywords = keywords

    def __call__(self, *args, **keywords):
        merged = dict(self.keywords)
        merged.update(keywords)
        return self.func(*self.args, *args, **merged)

    def __repr__(self):
        parts = [repr(self.func)]
        for a in self.args:
            parts.append(repr(a))
        for k in self.keywords:
            parts.append("%s=%r" % (k, self.keywords[k]))
        return "functools.partial(%s)" % ", ".join(parts)


class _CacheInfo:
    def __init__(self, hits, misses, maxsize, currsize):
        self.hits = hits
        self.misses = misses
        self.maxsize = maxsize
        self.currsize = currsize

    def __repr__(self):
        return "CacheInfo(hits=%r, misses=%r, maxsize=%r, currsize=%r)" % (self.hits, self.misses, self.maxsize, self.currsize)

    def __iter__(self):
        return iter((self.hits, self.misses, self.maxsize, self.currsize))

    def __getitem__(self, index):
        return (self.hits, self.misses, self.maxsize, self.currsize)[index]

    def __eq__(self, other):
        return tuple(self) == tuple(other)


def _make_key(args, keywords, typed):
    key = args
    if keywords:
        key = key + ("<keywords>",)
        for name in keywords:
            key = key + (name, keywords[name])
    if typed:
        key = key + tuple([type(v) for v in args])
        if keywords:
            key = key + tuple([type(keywords[name]) for name in keywords])
    return key


def _lru_cache_wrapper(user_function, maxsize, typed):
    # The results, oldest first: a dictionary keeps the order its keys
    # were added in, so the first key is the least recently used one.
    cache = {}
    counts = [0, 0]

    def wrapper(*args, **keywords):
        if maxsize == 0:
            counts[1] += 1
            return user_function(*args, **keywords)
        key = _make_key(args, keywords, typed)
        if key in cache:
            counts[0] += 1
            result = cache[key]
            if maxsize is not None:
                # (Used just now: it goes to the end.)
                del cache[key]
                cache[key] = result
            return result
        counts[1] += 1
        result = user_function(*args, **keywords)
        cache[key] = result
        if maxsize is not None and len(cache) > maxsize:
            for oldest in cache:
                break
            del cache[oldest]
        return result

    def cache_info():
        return _CacheInfo(counts[0], counts[1], maxsize, len(cache))

    def cache_clear():
        cache.clear()
        counts[0] = 0
        counts[1] = 0

    def cache_parameters():
        return {"maxsize": maxsize, "typed": typed}

    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache_clear
    wrapper.cache_parameters = cache_parameters
    return update_wrapper(wrapper, user_function)


def lru_cache(maxsize=128, typed=False):
    """Keeps a function's results: @lru_cache, @lru_cache(), @lru_cache(maxsize=None)."""
    if isinstance(maxsize, int):
        if maxsize < 0:
            maxsize = 0
    elif callable(maxsize) and isinstance(typed, bool):
        # @lru_cache with no parentheses: `maxsize` is the function.
        return _lru_cache_wrapper(maxsize, 128, typed)
    elif maxsize is not None:
        raise TypeError("Expected first argument to be an integer, a callable, or None")

    def decorating_function(user_function):
        return _lru_cache_wrapper(user_function, maxsize, typed)

    return decorating_function


def cache(user_function):
    """Keeps every result of a function: the same as lru_cache(maxsize=None)."""
    return lru_cache(maxsize=None)(user_function)


def cmp_to_key(mycmp):
    """A key function for sorted() from an old-style comparison function."""

    class K:
        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

    return K


def _has(cls, name):
    # (Defined by the class or one it inherits from: not what `object` gives.)
    return getattr(cls, name, None) is not None


def total_ordering(cls):
    """A class decorator: from __eq__ and one of < <= > >=, the other three."""
    defined = [op for op in ("__lt__", "__le__", "__gt__", "__ge__") if _has(cls, op)]
    if not defined:
        raise ValueError("must define at least one ordering operation: < > <= >=")
    root = defined[0]
    if root == "__lt__":
        if "__gt__" not in defined:
            cls.__gt__ = lambda self, other: not (self < other or self == other)
        if "__le__" not in defined:
            cls.__le__ = lambda self, other: self < other or self == other
        if "__ge__" not in defined:
            cls.__ge__ = lambda self, other: not self < other
    elif root == "__le__":
        if "__ge__" not in defined:
            cls.__ge__ = lambda self, other: not self <= other or self == other
        if "__lt__" not in defined:
            cls.__lt__ = lambda self, other: self <= other and not self == other
        if "__gt__" not in defined:
            cls.__gt__ = lambda self, other: not self <= other
    elif root == "__gt__":
        if "__lt__" not in defined:
            cls.__lt__ = lambda self, other: not (self > other or self == other)
        if "__ge__" not in defined:
            cls.__ge__ = lambda self, other: self > other or self == other
        if "__le__" not in defined:
            cls.__le__ = lambda self, other: not self > other
    else:
        if "__le__" not in defined:
            cls.__le__ = lambda self, other: not self >= other or self == other
        if "__gt__" not in defined:
            cls.__gt__ = lambda self, other: self >= other and not self == other
        if "__lt__" not in defined:
            cls.__lt__ = lambda self, other: not self >= other
    return cls
