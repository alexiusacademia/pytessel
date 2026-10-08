# Smaller gaps: keyword-only parameters, exec/eval namespaces, keys that
# compare by hash and equality, special methods of built-in values, a few
# str methods.


def attempt(f, *args, **kwargs):
    try:
        print(f(*args, **kwargs))
    except Exception as e:
        print(type(e).__name__ + ":", e)


# ---- keyword-only parameters ----
def after_star(*items, sep="-", end=None):
    return sep.join(str(i) for i in items) + (end or "")


print(after_star(1, 2, 3), after_star(1, 2, sep="+"), after_star(sep="x"), after_star(1, end="!"))


def bare_star(a, *, key, flag=False):
    return a, key, flag


print(bare_star(1, key=2), bare_star(1, key=2, flag=True), bare_star(a=1, key="k"))
attempt(bare_star, 1)
attempt(bare_star, 1, 2)
attempt(bare_star, 1, key=1, other=2)
attempt(bare_star, 1, 2, key=3)


def two_required(*, x, y):
    return x + y


attempt(two_required, x=1, y=2)
attempt(two_required)
attempt(two_required, x=1)


def everything(a, b=2, *rest, c, d=4, **more):
    return a, b, rest, c, d, sorted(more.items())


print(everything(1, c=3), everything(1, 20, 30, 40, c=3, d=5, e=6), everything(c=1, a=0))
attempt(everything, 1, 2, 3)
first = lambda *xs, scale=2: [x * scale for x in xs]
print(first(1, 2), first(1, scale=10))


class Widget:
    def __init__(self, name, *, size=1, color):
        self.name, self.size, self.color = name, size, color

    def resize(self, *, by):
        return self.size + by


w = Widget("w", color="red")
print(w.name, w.size, w.color, w.resize(by=2))
print("widget")


def gen(*, n):
    for i in range(n):
        yield i


print(list(gen(n=3)))
defaults_seen = []


def default_once(*, stamp=defaults_seen.append("evaluated") or "stamp"):
    return stamp


print(default_once(), default_once(), defaults_seen)

# ---- exec and eval with namespaces ----
ns = {"x": 5}
print(eval("x * 2", ns), eval("x + y", {"x": 1, "y": 2}), eval("x + y", {"x": 1}, {"y": 10}), eval("len(name)", {"name": "four"}))
exec("y = x + 1\nz = [y] * 2", ns)
print(ns["y"], ns["z"], sorted(k for k in ns if not k.startswith("__")))
attempt(eval, "x + missing", ns)
scope = {}
exec("def square(n):\n    return n * n\n\nclass Thing:\n    kind = 'thing'\n", scope)
print(scope["square"](7), scope["Thing"].kind, scope["Thing"]().kind)
scope["offset"] = 100
exec("def twice(n):\n    return helper(n) * 2\n\ndef helper(n):\n    return n + offset\n", scope)
print(scope["twice"](1))
x = "module x"
exec("seen = x", {"x": "namespace x"})
print(x, "seen" in globals())
g, l = {"a": 1}, {"b": 2}
exec("c = a + b\na = 50", g, l)
print(g["a"], sorted(l.items()))
exec("del gone", {"gone": 1})
attempt(exec, "print(x)", {})
attempt(exec, "x = ", {})
attempt(eval, "1 +", {})
attempt(exec, "x = 1", 5)
exec("made_global = 'here'")
print(made_global, eval("made_global.upper()"), eval("1 + 1"), eval("[i * 2 for i in range(3)]"))


def local_eval():
    hidden = "local"
    return eval("hidden + '!'"), eval("hidden", {"hidden": "from dict"})


print(local_eval())

# ---- keys go by hash, then equality ----
class Pair:
    def __init__(self, a, b):
        self.a, self.b = a, b

    def __eq__(self, other):
        if isinstance(other, Pair):
            return (self.a, self.b) == (other.a, other.b)
        if isinstance(other, tuple):
            return (self.a, self.b) == other
        return NotImplemented

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        return "Pair(%r, %r)" % (self.a, self.b)


table = {(1, 2): "tuple key"}
print(table[Pair(1, 2)], Pair(1, 2) in table, Pair(1, 3) in table, table.get(Pair(9, 9)))
table[Pair(1, 2)] = "set through a Pair"
print(table, len(table))
by_pair = {Pair("a", "b"): 1}
print(by_pair[("a", "b")], ("a", "b") in by_pair, ("a", "c") in by_pair, {Pair(1, 2), (1, 2), Pair(1, 2)} == {(1, 2)},
      len({Pair(1, 2), (1, 2), (2, 1)}))


class Name:
    def __init__(self, text):
        self.text = text

    def __eq__(self, other):
        return isinstance(other, Name) and self.text.lower() == other.text.lower()

    def __hash__(self):
        return hash(self.text.lower())


names = {Name("Ada"): 1}
names[Name("ADA")] = 2
names[Name("Bob")] = 3
print(len(names), names[Name("ada")], Name("bob") in names, Name("eve") in names)


class Unhashable:
    __hash__ = None


attempt(lambda: {Unhashable(): 1})
attempt(lambda: hash(Unhashable()))


class OnlyEq:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return isinstance(other, OnlyEq) and self.v == other.v

    __hash__ = None


attempt(lambda: {OnlyEq(1)})
print(OnlyEq(1) == OnlyEq(1), OnlyEq(1) in [OnlyEq(1)])

# ---- special methods of built-in values, by name ----
print(hasattr([], "__len__"), hasattr([], "__iter__"), hasattr(5, "__len__"), hasattr("s", "__getitem__"), hasattr({}, "__contains__"),
      hasattr(5, "__add__"), hasattr(None, "__iter__"), hasattr((), "__hash__"), hasattr(5, "__iter__"), hasattr(len, "__call__"),
      hasattr("s", "__mul__"), hasattr({}, "__setitem__"), hasattr((), "__setitem__"), hasattr(1.5, "__float__"))
print([1, 2, 3].__len__(), "abc".__len__(), {"a": 1}.__contains__("a"), [1, 2].__contains__(3), (5).__add__(2), (5).__sub__(7),
      "ab".__mul__(2), [1].__add__([2]), (2).__pow__(10), (7).__mod__(3), (1).__radd__(2), (10).__rsub__(1), (5).__eq__(5),
      (5).__lt__(3), "a".__ne__("b"), [3, 4].__getitem__(1), "xyz".__getitem__(-1), (1.5).__int__(), (3).__float__(),
      (-3).__abs__(), (3).__neg__(), "s".__repr__(), (5).__str__(), [1, 2].__repr__(), (0).__bool__())
items = [1, 2, 3]
items.__setitem__(0, 10)
items.__delitem__(1)
print(items, list(items.__iter__()), list(map((10).__add__, [1, 2])), sorted(["bb", "a"], key=str.__len__) if False else "skip")
length = [1, 2, 3].__len__
print(length(), callable(length), "x".__class__.__name__, (5).__class__ is int)
attempt(lambda: (5).__len__())
attempt(lambda: [].__nothing__)

# ---- int, str ----
print(int("101", base=2), int("ff", base=16), int("z", base=36), int("0x1f", base=0), int("12", 3), int(" 42 "))
attempt(lambda: int("12", base=2))
print(repr("a\tb\tc".expandtabs()), repr("a\tbcd\te".expandtabs(4)), repr("\tx".expandtabs(tabsize=2)), repr("ab\n\tc".expandtabs(3)),
      repr("no tabs".expandtabs()), repr("a\tb".expandtabs(0)))
table = str.maketrans("abc", "xyz")
print("aabbcc cab".translate(table), "hello".translate(str.maketrans("", "", "l")), "hello".translate(str.maketrans("el", "ip", "o")),
      "abc".translate({97: "A", 98: None, 99: 67}), "abc".translate(str.maketrans({"a": "1", "b": None})), sorted(table.items()))
attempt(lambda: str.maketrans("ab", "x"))
attempt(lambda: str.maketrans("ab"))
print("a\nb\r\nc\rd".splitlines(), "a\nb\r\nc\rd\n".splitlines(True), "one".splitlines(), "".splitlines(), "\n".splitlines(),
      "a\n\nb".splitlines(keepends=True), "x\n".splitlines())
print(repr("\x00"), repr("\x1b[0m"), repr("a\x07b"), repr("\x7f"), repr("tab\t nl\n cr\r"), repr("q'\x01"), ["\x00\x1f"], repr("é ü"),
      repr("\x80\xa0"), repr("back\\slash"))
print(issubclass(MemoryError, Exception), MemoryError("big").args)
