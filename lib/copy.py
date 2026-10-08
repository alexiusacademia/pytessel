# copy: shallow and deep copies of values.
#
# Author: Alexius Academia
# Date: 2026-10-08
import _pytessel


class Error(Exception):
    pass


error = Error

_ATOMIC = (int, float, bool, str, range, type)
_ATOMIC_NAMES = ("NoneType", "function", "builtin_function_or_method", "method", "module")


def _is_atomic(x):
    # Values that can't change (and functions, classes, modules): a copy
    # of one is the value itself.
    return isinstance(x, _ATOMIC) or type(x).__name__ in _ATOMIC_NAMES


def _new_like(x):
    # An object of x's class, made without calling __init__.
    return _pytessel.new_instance(type(x))


def copy(x):
    """A new object with the same contents (the contents aren't copied)."""
    if isinstance(x, list):
        return list(x)
    if isinstance(x, dict):
        return dict(x)
    if isinstance(x, set):
        return set(x)
    if isinstance(x, tuple) or _is_atomic(x):
        return x
    copier = getattr(x, "__copy__", None)
    if copier is not None:
        return copier()
    if not hasattr(x, "__dict__"):
        return x
    made = _new_like(x)
    for name in x.__dict__:
        setattr(made, name, x.__dict__[name])
    return made


def deepcopy(x, memo=None):
    """A new object whose contents are copies too, all the way down."""
    if memo is None:
        memo = {}
    if isinstance(x, (list, dict, set, tuple)):
        key = id(x)
        if key in memo:
            return memo[key]
        if isinstance(x, list):
            made = []
            memo[key] = made
            for item in x:
                made.append(deepcopy(item, memo))
            return made
        if isinstance(x, dict):
            made = {}
            memo[key] = made
            for k in x:
                made[deepcopy(k, memo)] = deepcopy(x[k], memo)
            return made
        if isinstance(x, set):
            made = set()
            memo[key] = made
            for item in x:
                made.add(deepcopy(item, memo))
            return made
        items = [deepcopy(item, memo) for item in x]
        # (A tuple of things that can't change is the tuple itself.)
        same = True
        for i in range(len(items)):
            if items[i] is not x[i]:
                same = False
        made = x if same else tuple(items)
        memo[key] = made
        return made
    if _is_atomic(x):
        return x
    key = id(x)
    if key in memo:
        return memo[key]
    copier = getattr(x, "__deepcopy__", None)
    if copier is not None:
        made = copier(memo)
        memo[key] = made
        return made
    if not hasattr(x, "__dict__"):
        return x
    made = _new_like(x)
    memo[key] = made
    for name in x.__dict__:
        setattr(made, name, deepcopy(x.__dict__[name], memo))
    return made
