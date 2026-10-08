# itertools: functions that make and combine iterators.
#
# Author: Alexius Academia
# Date: 2026-10-08
#
# Written as generators, the way Python's documentation shows what each
# one is "roughly equivalent to". The ones that never end (count, cycle,
# repeat with no times) need generators that run a step at a time.
#
# A function that checks its arguments does it before making its
# generator, so that a wrong call fails where it's made.


def count(start=0, step=1):
    """start, start + step, start + 2 * step, … without end."""
    n = start
    while True:
        yield n
        n += step


def cycle(iterable):
    """The items again and again, without end."""
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
    while saved:
        for element in saved:
            yield element


def repeat(object, times=None):
    """The same object, `times` times (or without end)."""
    if times is None:
        while True:
            yield object
    else:
        for i in range(times):
            yield object


def accumulate(iterable, func=None, initial=None):
    """Running totals (or running results of `func`)."""
    it = iter(iterable)
    total = initial
    if initial is None:
        try:
            total = next(it)
        except StopIteration:
            return
    yield total
    for element in it:
        if func is None:
            total = total + element
        else:
            total = func(total, element)
        yield total


def chain(*iterables):
    """The items of the first iterable, then of the second, …"""
    for it in iterables:
        for element in it:
            yield element


def _chain_from_iterable(iterables):
    for it in iterables:
        for element in it:
            yield element


chain.from_iterable = _chain_from_iterable


def compress(data, selectors):
    """The items of data whose selector is true."""
    for d, s in zip(data, selectors):
        if s:
            yield d


def dropwhile(predicate, iterable):
    """The items from the first one the predicate is false for."""
    dropping = True
    for x in iterable:
        if dropping and predicate(x):
            continue
        dropping = False
        yield x


def takewhile(predicate, iterable):
    """The items before the first one the predicate is false for."""
    for x in iterable:
        if predicate(x):
            yield x
        else:
            break


def filterfalse(predicate, iterable):
    """The items the predicate is false for."""
    for x in iterable:
        if predicate is None:
            if not x:
                yield x
        elif not predicate(x):
            yield x


def groupby(iterable, key=None):
    """(key, group) for each run of items that have the same key."""
    started = False
    current = None
    group = []
    for element in iterable:
        k = element if key is None else key(element)
        if not started:
            started = True
            current = k
        elif k != current:
            yield (current, iter(group))
            current = k
            group = []
        group.append(element)
    if started:
        yield (current, iter(group))


def _islice(iterable, start, stop, step):
    wanted = start
    i = 0
    for element in iterable:
        if i == wanted:
            yield element
            wanted += step
            if stop is not None and wanted >= stop:
                return
        i += 1


def _is_index(value):
    return isinstance(value, int) and value >= 0


def islice(iterable, *args):
    """islice(it, stop) or islice(it, start, stop[, step]): a slice of an iterator."""
    if len(args) == 0:
        raise TypeError("islice expected at least 2 arguments, got 1")
    if len(args) > 3:
        raise TypeError("islice expected at most 4 arguments, got %d" % (len(args) + 1))
    start = 0
    step = 1
    if len(args) == 1:
        stop = args[0]
        if stop is not None and not _is_index(stop):
            raise ValueError("Stop argument for islice() must be None or an integer: 0 <= x <= sys.maxsize.")
    else:
        start = 0 if args[0] is None else args[0]
        stop = args[1]
        if not _is_index(start):
            raise ValueError("Indices for islice() must be None or an integer: 0 <= x <= sys.maxsize.")
        if stop is not None and not _is_index(stop):
            raise ValueError("Stop argument for islice() must be None or an integer: 0 <= x <= sys.maxsize.")
        if len(args) == 3 and args[2] is not None:
            step = args[2]
            if not isinstance(step, int) or step < 1:
                raise ValueError("Step for islice() must be a positive integer or None.")
    if stop is not None and stop <= start:
        return iter(())
    return _islice(iterable, start, stop, step)


def pairwise(iterable):
    """(first, second), (second, third), …"""
    started = False
    a = None
    for b in iterable:
        if started:
            yield (a, b)
        started = True
        a = b


def starmap(function, iterable):
    """function(*args) for each args of the iterable."""
    for args in iterable:
        yield function(*args)


def _zip_longest(iterators, fillvalue):
    active = len(iterators)
    if not active:
        return
    done = [False] * active
    while True:
        values = []
        for i in range(len(iterators)):
            value = fillvalue
            if not done[i]:
                try:
                    value = next(iterators[i])
                except StopIteration:
                    done[i] = True
                    active -= 1
                    if not active:
                        return
                    value = fillvalue
            values.append(value)
        yield tuple(values)


def zip_longest(*iterables, **kwargs):
    """Like zip, to the end of the longest one: fillvalue where one ran out."""
    fillvalue = kwargs.pop("fillvalue", None)
    if kwargs:
        raise TypeError("zip_longest() got an unexpected keyword argument")
    return _zip_longest([iter(it) for it in iterables], fillvalue)


def _product(pools):
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def product(*iterables, **kwargs):
    """Every way to take one item from each iterable."""
    repeat = kwargs.pop("repeat", 1)
    if kwargs:
        raise TypeError("product() got an unexpected keyword argument")
    if not isinstance(repeat, int):
        raise TypeError("'%s' object cannot be interpreted as an integer" % type(repeat).__name__)
    if repeat < 0:
        raise ValueError("repeat argument cannot be negative")
    return _product([tuple(pool) for pool in iterables] * repeat)


def _permutations(pool, r):
    n = len(pool)
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n - r, -1))
    yield tuple([pool[k] for k in indices[:r]])
    while n:
        found = False
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple([pool[k] for k in indices[:r]])
                found = True
                break
        if not found:
            return


def permutations(iterable, r=None):
    """Every way to put r of the items in order."""
    pool = tuple(iterable)
    if r is None:
        r = len(pool)
    if not isinstance(r, int):
        raise TypeError("Expected int as r")
    if r < 0:
        raise ValueError("r must be non-negative")
    return _permutations(pool, r)


def _combinations(pool, r):
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple([pool[k] for k in indices])
    while True:
        found = False
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                found = True
                break
        if not found:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield tuple([pool[k] for k in indices])


def combinations(iterable, r):
    """Every way to choose r of the items, in the order they come."""
    pool = tuple(iterable)
    if not isinstance(r, int):
        raise TypeError("'%s' object cannot be interpreted as an integer" % type(r).__name__)
    if r < 0:
        raise ValueError("r must be non-negative")
    return _combinations(pool, r)


def _combinations_with_replacement(pool, r):
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple([pool[k] for k in indices])
    while True:
        found = False
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                found = True
                break
        if not found:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple([pool[k] for k in indices])


def combinations_with_replacement(iterable, r):
    """Every way to choose r of the items, where an item may be chosen again."""
    pool = tuple(iterable)
    if not isinstance(r, int):
        raise TypeError("'%s' object cannot be interpreted as an integer" % type(r).__name__)
    if r < 0:
        raise ValueError("r must be non-negative")
    return _combinations_with_replacement(pool, r)


def _batched(iterable, n):
    batch = []
    for element in iterable:
        batch.append(element)
        if len(batch) == n:
            yield tuple(batch)
            batch = []
    if batch:
        yield tuple(batch)


def batched(iterable, n):
    """The items in tuples of n (the last one may be shorter)."""
    if n < 1:
        raise ValueError("n must be at least one")
    return _batched(iterable, n)


def _tee_one(it, mine, buffers):
    while True:
        if not mine:
            try:
                value = next(it)
            except StopIteration:
                return
            for buffer in buffers:
                buffer.append(value)
        yield mine.pop(0)


def tee(iterable, n=2):
    """n iterators that each give the iterable's items."""
    if n < 0:
        raise ValueError("n must be >= 0")
    it = iter(iterable)
    buffers = [[] for i in range(n)]
    return tuple([_tee_one(it, mine, buffers) for mine in buffers])
