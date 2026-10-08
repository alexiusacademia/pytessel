# bisect: keeping a list in order without sorting it again.
#
# Author: Alexius Academia
# Date: 2026-10-08


def bisect_right(a, x, lo=0, hi=None, key=None):
    """The place to put x in the sorted list a, after any items equal to it."""
    if lo < 0:
        raise ValueError("lo must be non-negative")
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        item = a[mid] if key is None else key(a[mid])
        if x < item:
            hi = mid
        else:
            lo = mid + 1
    return lo


def bisect_left(a, x, lo=0, hi=None, key=None):
    """The place to put x in the sorted list a, before any items equal to it."""
    if lo < 0:
        raise ValueError("lo must be non-negative")
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        item = a[mid] if key is None else key(a[mid])
        if item < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def insort_right(a, x, lo=0, hi=None, key=None):
    """Puts x in the sorted list a, after any items equal to it."""
    if key is None:
        lo = bisect_right(a, x, lo, hi)
    else:
        lo = bisect_right(a, key(x), lo, hi, key=key)
    a.insert(lo, x)


def insort_left(a, x, lo=0, hi=None, key=None):
    """Puts x in the sorted list a, before any items equal to it."""
    if key is None:
        lo = bisect_left(a, x, lo, hi)
    else:
        lo = bisect_left(a, key(x), lo, hi, key=key)
    a.insert(lo, x)


bisect = bisect_right
insort = insort_right
