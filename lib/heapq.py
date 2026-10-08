# heapq: a list kept as a heap, whose smallest item is always first.
#
# Author: Alexius Academia
# Date: 2026-10-08


def heappush(heap, item):
    """Adds an item to the heap."""
    heap.append(item)
    _siftdown(heap, 0, len(heap) - 1)


def heappop(heap):
    """Takes the smallest item off the heap."""
    if not heap:
        raise IndexError("index out of range")
    last = heap.pop()
    if heap:
        smallest = heap[0]
        heap[0] = last
        _siftup(heap, 0)
        return smallest
    return last


def heapreplace(heap, item):
    """Takes the smallest item off, and puts `item` on."""
    if not heap:
        raise IndexError("index out of range")
    smallest = heap[0]
    heap[0] = item
    _siftup(heap, 0)
    return smallest


def heappushpop(heap, item):
    """Puts `item` on, then takes the smallest item off."""
    if heap and heap[0] < item:
        smallest = heap[0]
        heap[0] = item
        _siftup(heap, 0)
        return smallest
    return item


def heapify(x):
    """Makes a list a heap, in place."""
    n = len(x)
    for i in reversed(range(n // 2)):
        _siftup(x, i)


def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem


def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    childpos = 2 * pos + 1
    while childpos < endpos:
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2 * pos + 1
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)


def merge(*iterables, **kwargs):
    """Several sorted iterables as one sorted iterator."""
    key = kwargs.pop("key", None)
    reverse = kwargs.pop("reverse", False)
    if kwargs:
        raise TypeError("merge() got an unexpected keyword argument")
    # (sorted() keeps the order of equal items, as merge does.)
    items = []
    for it in iterables:
        for element in it:
            items.append(element)
    return iter(sorted(items, key=key, reverse=reverse))


def nsmallest(n, iterable, key=None):
    """The n smallest items, smallest first."""
    if n <= 0:
        return []
    return sorted(iterable, key=key)[:n]


def nlargest(n, iterable, key=None):
    """The n largest items, largest first."""
    if n <= 0:
        return []
    return sorted(iterable, key=key, reverse=True)[:n]
