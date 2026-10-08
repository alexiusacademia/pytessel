# slice objects and Ellipsis.


def attempt(f):
    try:
        print(f())
    except Exception as e:
        print(type(e).__name__ + ":", e)


# ---- making them, their parts, repr ----
s = slice(1, 5, 2)
print(s, s.start, s.stop, s.step)
print(slice(3), slice(1, 3), slice(None), slice(None, None, -1), slice(0, 10, None))
print(slice(3).start, slice(3).stop, slice(3).step)
print(repr(slice(1, 2)), str(slice(1, 2, 3)), [slice(1)], (slice(1, 2),))
print(slice("a", "z"), slice(1.5, 2.5), slice((1, 2), [3]), slice(slice(1), 2).start)
print(type(s), type(s).__name__, isinstance(s, slice), isinstance(3, slice), slice)
print(bool(slice(0)), bool(slice(None)))
attempt(lambda: slice())
attempt(lambda: slice(1, 2, 3, 4))
attempt(lambda: s.nothing)

# ---- equality, ordering, hashing ----
print(slice(1, 2) == slice(1, 2), slice(1, 2) == slice(1, 2, None), slice(1, 2) == slice(1, 3), slice(1, 2) != slice(1, 2))
print(slice(2) == slice(None, 2), slice(1, 2) == (1, 2, None), slice(1, 2) == 5, slice(1) is slice(1), s is s)
print(slice(1, 2) < slice(1, 3), slice(2, 2) < slice(1, 3), slice(1, 2, 3) <= slice(1, 2, 3), slice(1, 2) > slice(0, 9))
table = {slice(1, 2): "a", slice(None): "all"}
print(table[slice(1, 2)], table[slice(None, None, None)], slice(1, 2) in table, slice(1, 3) in table)
print(len({slice(1), slice(1), slice(2)}), hash(slice(1, 2)) == hash(slice(1, 2)))
attempt(lambda: {slice([1]): 0})

# ---- indices ----
print(slice(1, 5).indices(10), slice(None).indices(4), slice(None, None, -1).indices(4), slice(-3, None).indices(10))
print(slice(100).indices(5), slice(-100, 100).indices(5), slice(2, 1).indices(5), slice(None, None, 2).indices(7))
print(slice(5, 0, -2).indices(10), slice(None, -100, -1).indices(5), slice(100, None, -1).indices(5), slice(-1, None, -1).indices(0))
print(slice(0).indices(0), slice(3, None).indices(2), slice(True, 3).indices(5))
attempt(lambda: slice(1, 2, 0).indices(5))
attempt(lambda: slice(1).indices(-1))
attempt(lambda: slice("a").indices(5))
attempt(lambda: slice(1).indices("x"))
attempt(lambda: slice(1).indices())
for sl in [slice(None), slice(1, 4), slice(None, None, -1), slice(-2, None), slice(5, 1, -2), slice(10, 20)]:
    print(sl, [list(range(8))[i] for i in range(*sl.indices(8))] == list(range(8))[sl])

# ---- on lists, tuples, strings, bytes, ranges ----
xs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(xs[slice(2, 5)], xs[slice(None, 3)], xs[slice(-3, None)], xs[slice(None, None, 2)], xs[slice(None, None, -1)])
print(xs[slice(7, 2, -2)], xs[slice(20)], xs[slice(5, 2)], xs[slice(None)], xs[s], xs[slice(True, 4)])
t = tuple(xs)
print(t[slice(2, 5)], t[slice(None, None, 3)], type(t[slice(1, 2)]), t[slice(-1, None)])
text = "hello world"
print(text[slice(5)], text[slice(6, None)], text[slice(None, None, -1)], text[slice(1, 9, 3)], repr(text[slice(4, 4)]))
print(b"hello world"[slice(5)], b"hello"[slice(None, None, -1)], bytearray(b"abcdef")[slice(1, 5, 2)])
print(range(10)[slice(2, 8, 2)], range(10)[slice(None, None, -1)], range(0, 20, 3)[slice(1, 4)], range(5)[slice(10)])
print(range(10)[2:5], range(10)[::-2], range(10)[5:2], list(range(10)[-3:]), range(10)[::3][1], len(range(100)[10:50:7]))
print(type(range(10)[1:3]), range(10)[1:3] == range(1, 3), list(range(3, 30, 4)[::-1]), range(10, 0, -1)[2:6:2])
whole = slice(None)
head = slice(3)
tail = slice(-2, None)
every_other = slice(None, None, 2)
for name, sl in [("whole", whole), ("head", head), ("tail", tail), ("every_other", every_other)]:
    print(name, xs[sl], text[sl], t[sl])
attempt(lambda: xs[slice(1, 2, 0)])
attempt(lambda: xs[slice("a", "b")])
attempt(lambda: xs[slice(1.0, 2)])
attempt(lambda: text[slice(None, None, 0)])
attempt(lambda: xs[1.5:3])
five, pair, nothing, dots = 5, {1, 2}, None, ...
attempt(lambda: five[slice(1)])
attempt(lambda: {1: 2}[slice(1)])
attempt(lambda: {"a": 1}[1:2])
attempt(lambda: pair[slice(1)])
attempt(lambda: nothing[1:2])

# ---- assigning and deleting through slice objects ----
ys = list(range(10))
ys[slice(2, 5)] = ["a", "b"]
print(ys)
ys[slice(None, None, 3)] = ["x", "y", "z"]
print(ys)
ys[slice(0, 0)] = [100, 200]
print(ys)
del ys[slice(0, 2)]
print(ys)
del ys[slice(None, None, 2)]
print(ys)
del ys[slice(None)]
print(ys)
zs = list(range(10))
del zs[::3]
print(zs)
del zs[1:3]
print(zs)
del zs[::-1]
print(zs)
zs = list(range(6))
zs[::2] = "abc"
zs[1::2] = (10, 20, 30)
print(zs)
zs[1:1] = zs[::-1]
print(zs)
ba = bytearray(b"0123456789")
ba[slice(2, 4)] = b"--"
del ba[slice(None, None, 4)]
print(ba)


def assign(target, index, value):
    try:
        target[index] = value
        print(target)
    except Exception as e:
        print(type(e).__name__ + ":", e)


def delete(target, index):
    try:
        del target[index]
        print(target)
    except Exception as e:
        print(type(e).__name__ + ":", e)


assign([1, 2, 3, 4], slice(None, None, 2), [9])
assign([1, 2, 3, 4], slice(None, None, 2), [])
assign([1, 2, 3, 4], slice(1, 3), [])
assign([1, 2, 3, 4], slice(1, 3), 5)
assign((1, 2, 3), slice(1), [9])
assign("abc", slice(1), "x")
assign({}, slice(1, 2), "kept under a slice")
delete((1, 2, 3), slice(1))
delete("abc", slice(1))
delete([1, 2, 3], slice(None, None, 0))
delete({slice(1): 1, 2: 2}, slice(1))


# ---- a class's __getitem__, __setitem__ and __delitem__ get the slice ----
class Recorder:
    def __getitem__(self, key):
        return "get %r" % (key,)

    def __setitem__(self, key, value):
        print("set %r = %r" % (key, value))

    def __delitem__(self, key):
        print("del %r" % (key,))


r = Recorder()
print(r[1], r[1:2], r[:], r[::2], r[1:], r[:-1], r[1:10:3], r["a":"z"], r[None:None], r[1.5:2.5])
print(r[1, 2], r[1:2, 3], r[1:2, ::3], r[:, :], r[..., 0], r[...], r[1:2, ..., None], r[(1, 2)], r[1, ])
print(r[slice(1, 2)], r[s], r[r[1]:2], r[1 + 1:2 * 3], r[-1:], r[lambda: 0 if True else 1] != "", r[x := 5], x)
r[1:2] = "a"
r[::2] = [1, 2]
r[1:2, 3:4] = None
r[...] = 0
del r[1:2]
del r[:, 1]
del r[...]
r[1:2] += "!"


class Matrix:
    def __init__(self, rows):
        self.rows = rows

    def __getitem__(self, key):
        if isinstance(key, tuple):
            row, column = key
            picked = self.rows[row]
            if isinstance(row, slice):
                return [line[column] for line in picked]
            return picked[column]
        return self.rows[key]

    def __setitem__(self, key, value):
        row, column = key
        self.rows[row][column] = value


m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(m[0], m[1, 1], m[0, 1:], m[1:, 0], m[:, ::2], m[::2, ::2], m[-1, ::-1], m[1:])
m[0, 0] = 100
m[2, 1:] = [80, 90]
print(m.rows)


class Window:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return Window([self.items[i] for i in range(start, stop, step)])
        if key < 0:
            key += len(self)
        if not 0 <= key < len(self):
            raise IndexError("window index out of range")
        return self.items[key]

    def __repr__(self):
        return "Window(%r)" % (self.items,)


w = Window(list("abcdefgh"))
print(w[2], w[-1], w[2:5], w[::-1], w[::3], w[5:], w[:2][1], w[1:7][::2][-1], list(w[6:]))
attempt(lambda: w[20])


class Index:
    def __init__(self, n):
        self.n = n

    def __index__(self):
        return self.n


print(xs[Index(2):Index(5)], xs[slice(Index(1), None, Index(4))], text[:Index(4)], slice(Index(1), Index(3)).indices(10))

# ---- Ellipsis ----
print(..., Ellipsis, repr(...), str(Ellipsis), type(...), type(...).__name__)
print(... is Ellipsis, ... == Ellipsis, ... is None, ... == 0, bool(...), [..., 1], {...: "dots"}[...], ... in (1, ...))
e = ...
print(e, e is ..., "set" if e is not None else "unset", hash(...) == hash(Ellipsis))


def later(): ...


class Empty: ...


print(later(), Empty.__name__)


def default(x=...):
    return "nothing given" if x is ... else x


print(default(), default(None), default(0))
attempt(lambda: ... + 1)
attempt(lambda: dots[0])
attempt(lambda: len(...))
