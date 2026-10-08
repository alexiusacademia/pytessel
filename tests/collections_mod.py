# The collections module: Counter, defaultdict, OrderedDict, deque,
# namedtuple, ChainMap.
#
# Author: Alexius Academia
# Date: 2026-10-08
import collections
from collections import Counter, defaultdict, OrderedDict, deque, namedtuple, ChainMap

# ---- Counter ----
c = Counter("abracadabra")
print(c)
print(c["a"], c["b"], c["z"], "z" in c, "a" in c, len(c))
print(c.most_common(2), c.most_common(), c.most_common(0))
print(sorted(c), sorted(c.items()), sorted(c.values()), sum(c.values()))
print(sorted(c.elements()))
print(Counter(), Counter([]), bool(Counter()), bool(c))
print(Counter(a=3, b=1), Counter({"x": 2, "y": 5}), Counter(["x", "y", "x"]))
words = "the quick brown fox jumps over the lazy dog the end".split()
wc = Counter(words)
print(wc.most_common(1), wc["the"], wc["cat"], len(wc))
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
print(c + d)
print(c - d)
print(c & d)
print(c | d)
print(+c, -c)
c.subtract(d)
print(c)
c.update("aab")
print(c)
c.update({"a": 10, "q": 1})
print(c)
c.update(z=5)
print(c["z"], c["a"])
c.subtract("aa")
c.subtract(a=1, b=1)
print(c["a"], c["b"])
c = Counter("aabbb")
c["c"] += 2
c["a"] -= 5
c["new"] = 7
print(c, list(c.elements()))
del c["new"]
print("new" in c, c["new"], len(c))
try:
    del c["never"]
except KeyError as e:
    print("KeyError", e)
print(c.pop("c"), c.get("c"), c.get("c", "none"), c.get("b"))
c.clear()
print(c, len(c))
c = Counter("hello")
copy = c.copy()
copy["h"] += 10
print(c["h"], copy["h"], c == Counter("olleh"), c == copy, c != copy, c == {"h": 1, "e": 1, "l": 2, "o": 1})
print(dict(c), list(c.keys()), list(c.values()), dict(c.most_common()))
total = Counter()
for chunk in ["ab", "bc", "cd"]:
    total += Counter(chunk)
print(total)
total -= Counter("bc")
print(total)
c = Counter(a=2, b=-1)
c += Counter()
print(c)
c = Counter(a=3, b=1)
c &= Counter(a=1, b=5)
print(c)
c |= Counter(a=4, c=2)
print(c)
print(Counter([1, 1, 2.0, 2, True]), Counter([(1, 2), (1, 2), (3,)]))
print(max(Counter("mississippi").items(), key=lambda p: p[1]))
print([k for k, n in Counter("mississippi").most_common() if n > 1])
print(Counter("aab") + Counter("bcc") == Counter("abbcac"), Counter("a") == Counter("b"))
print(Counter(Counter("aab")), Counter({"a": 0}), Counter(a=0) == Counter())
try:
    Counter("a") + {"a": 1}
except TypeError as e:
    print("TypeError", e)
try:
    Counter.fromkeys("ab")
except NotImplementedError as e:
    print("NotImplementedError", e)
letters = Counter()
for word in ["apple", "pear"]:
    for ch in word:
        letters[ch] += 1
print(letters.most_common(3))

# ---- defaultdict ----
dd = defaultdict(list)
for key, value in [("a", 1), ("b", 2), ("a", 3)]:
    dd[key].append(value)
print(dd, dict(dd), len(dd), sorted(dd), list(dd.items()))
print(dd["a"], dd["zzz"], "zzz" in dd, "nope" in dd, dd.get("nope"), dd.get("nope", 5), len(dd))
counts = defaultdict(int)
for ch in "mississippi":
    counts[ch] += 1
print(counts, counts["x"], sorted(counts.items()))
print(defaultdict(int), defaultdict(), defaultdict(None, {"a": 1}), defaultdict(list, [("k", [1])]), defaultdict(int, a=1))
groups = defaultdict(set)
for n in range(10):
    groups[n % 3].add(n)
print({k: sorted(v) for k, v in groups.items()})
nested = defaultdict(lambda: defaultdict(int))
nested["x"]["y"] += 1
nested["x"]["z"] += 2
print(dict(nested["x"]), list(nested), nested["x"]["y"])
plain = defaultdict(None)
try:
    plain["missing"]
except KeyError as e:
    print("KeyError", e)
print(dd.default_factory is list, counts.default_factory is int, plain.default_factory)
dd2 = dd.copy()
dd2["a"].append(99)
dd2["only"] = [1]
print(dd["a"], "only" in dd, dd2.default_factory is list)
print(dd == dd2, dd == {"a": [1, 3, 99], "b": [2], "zzz": []}, defaultdict(int) == {})
print(dd.pop("b"), dd.setdefault("s", "v"), dd.setdefault("s", "w"), sorted(dd.keys()))
dd.update({"u": 1}, w=2)
del dd["a"]
print(sorted(dd.items(), key=lambda p: p[0]), [k for k in dd])
dd.clear()
print(len(dd), bool(dd), dd)
try:
    defaultdict(5)
except TypeError as e:
    print("TypeError", e)
tree = defaultdict(lambda: "leaf")
print(tree["a"], tree["b"], len(tree), tree.get("c"), len(tree))
index = defaultdict(list)
for position, word in enumerate("to be or not to be".split()):
    index[word].append(position)
print(dict(index))

# ---- OrderedDict ----
od = OrderedDict()
od["one"] = 1
od["two"] = 2
od["three"] = 3
print(od, list(od), list(od.keys()), list(od.values()), list(od.items()), len(od))
od.move_to_end("one")
print(list(od))
od.move_to_end("three", last=False)
print(list(od))
od.move_to_end("two", False)
print(list(od))
print(od.popitem(), od.popitem(last=False), od)
od["x"] = 9
od["three"] = 33
print(od, od["x"], "x" in od, od.get("y"), od.pop("x"), list(od))
print(OrderedDict([("a", 1), ("b", 2)]), OrderedDict(a=1), OrderedDict({"k": "v"}), OrderedDict())
a = OrderedDict([("a", 1), ("b", 2)])
b = OrderedDict([("b", 2), ("a", 1)])
print(a == b, a == OrderedDict([("a", 1), ("b", 2)]), a == {"b": 2, "a": 1}, {"b": 2, "a": 1} == a, a != b)
print(list(reversed(a)), dict(a), sorted(b), list(a.copy().items()), a.copy() == a)
a.update({"c": 3})
a.setdefault("d", 4)
del a["a"]
print(a, len(a), bool(a), bool(OrderedDict()))
print(OrderedDict.fromkeys("abc"), OrderedDict.fromkeys("ab", 0))
try:
    a.move_to_end("nope")
except KeyError as e:
    print("KeyError", e)
try:
    OrderedDict().popitem()
except KeyError as e:
    print("KeyError", e)
try:
    a["nope"]
except KeyError as e:
    print("KeyError", e)
# A cache that forgets what was used longest ago.
cache = OrderedDict()
for key in ["a", "b", "c", "a", "d", "b", "e"]:
    if key in cache:
        cache.move_to_end(key)
    cache[key] = True
    if len(cache) > 3:
        cache.popitem(last=False)
print(list(cache))
a.clear()
print(a)

# ---- deque ----
d = deque([1, 2, 3])
d.append(4)
d.appendleft(0)
print(d, len(d), d[0], d[-1], d[2], list(d), 3 in d, 9 in d)
print(d.pop(), d.popleft(), d)
d.extend([7, 8])
d.extendleft([-1, -2])
print(d)
d.rotate(2)
print(d)
d.rotate(-3)
print(d)
d.rotate()
print(d)
d.rotate(0)
d.rotate(70)
print(d)
print(deque(), deque("abc"), deque(range(3)), bool(deque()), bool(d))
d = deque("abcdef")
d[0] = "A"
d[-1] = "F"
del d[1]
print(d, d.index("d"), d.count("c"), list(reversed(d)))
d.remove("c")
d.insert(1, "x")
d.reverse()
print(d, d.copy() == d, d == deque("FedxA"), d != deque("z"), d == list(d))
d.clear()
print(d, len(d))
recent = deque(maxlen=3)
for n in range(6):
    recent.append(n)
print(recent, recent.maxlen, deque([1, 2, 3, 4, 5], maxlen=2), deque("abcd", 2), deque(maxlen=0))
recent.appendleft(9)
print(recent)
recent.extend([7, 8])
print(recent)
recent.extendleft("xy")
print(recent, len(recent))
empty = deque(maxlen=0)
empty.append(1)
empty.appendleft(2)
print(empty, len(empty), deque([1, 2]).maxlen)
for bad in ["pop", "popleft"]:
    try:
        getattr(deque(), bad)()
    except IndexError as e:
        print("IndexError", e)
try:
    deque([1])[5]
except IndexError as e:
    print("IndexError", e)
try:
    deque([1]).remove(2)
except ValueError as e:
    print("ValueError", e)
try:
    deque([1]).index(2)
except ValueError as e:
    print("ValueError", e)
try:
    deque([1, 2], maxlen=2).insert(0, 5)
except IndexError as e:
    print("IndexError", e)
try:
    deque([1], maxlen=-1)
except ValueError as e:
    print("ValueError", e)
queue = deque()
for n in range(100):
    queue.append(n)
total = 0
while queue:
    total += queue.popleft()
print(total, len(queue), queue)
big = deque(range(1000))
for _ in range(990):
    big.popleft()
big.appendleft("front")
print(big, big[0], big[1], big[-1], len(big))
print(deque([1, 2]) + deque([3]), deque([1, 2]) * 2, deque([1, 2]) < deque([1, 3]), sum(deque([1, 2, 3])), max(deque([4, 9, 2])))
d = deque([1, 2])
d += [3, 4]
print(d, sorted(deque([3, 1, 2])), [x * 2 for x in d], list(enumerate(deque("ab"))), "".join(deque("xyz")))
a, b, *rest = deque([1, 2, 3, 4])
print(a, b, rest, tuple(deque([1])), list(zip(deque([1, 2]), deque("ab"))))


def bfs(graph, start):
    seen = [start]
    todo = deque([start])
    while todo:
        node = todo.popleft()
        for other in graph[node]:
            if other not in seen:
                seen.append(other)
                todo.append(other)
    return seen


print(bfs({"a": ["b", "c"], "b": ["d"], "c": ["d", "e"], "d": [], "e": ["a"]}, "a"))


def tail(lines, n):
    return list(deque(lines, maxlen=n))


print(tail(["l1", "l2", "l3", "l4"], 2), tail([], 2))

# ---- namedtuple ----
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p, p.x, p.y, p[0], p[1], p[-1], len(p), list(p), tuple(p))
x, y = p
print(x, y, p == (3, 4), (3, 4) == p, p == Point(3, 4), p != Point(4, 3), p == (3, 5), p == [3, 4])
print(Point._fields, p._asdict(), p._replace(x=10), p._replace(y=0, x=0), p)
print(Point._make([7, 8]), Point(y=1, x=2), Point(5, y=6), Point.__name__, type(p).__name__)
print(p < Point(3, 5), p > (1, 100), sorted([Point(2, 1), Point(1, 9), Point(1, 2)]), max(Point(1, 2), Point(1, 3)))
print(p + (5,), p * 2, 4 in p, 7 in p, p.count(3), p.index(4), sum(p), hash(p) == hash(Point(3, 4)))
print({p: "here"}[Point(3, 4)], {Point(1, 2), Point(1, 2), Point(2, 1)} == {Point(2, 1), Point(1, 2)})
Person = namedtuple("Person", "name age city")
ann = Person("Ann", 30, "Oslo")
print(ann, ann.name, ann.age, ann.city, Person._fields)
Pair = namedtuple("Pair", "left, right")
print(Pair(1, 2), Pair._fields)
Color = namedtuple("Color", "r g b alpha", defaults=[0, 255])
print(Color(1, 2), Color(1, 2, 3), Color(1, 2, 3, 4), Color._field_defaults)
Empty = namedtuple("Empty", [])
print(Empty(), len(Empty()), Empty._fields)
Renamed = namedtuple("Renamed", ["ok", "class", "ok", "_x", "2nd"], rename=True)
print(Renamed._fields, Renamed(1, 2, 3, 4, 5))
print([name for name, age, city in [ann, Person("Bo", 5, "Rome")]], "%s is %d" % (ann.name, ann.age))
print([p.x for p in map(Point._make, [(1, 2), (3, 4)])], dict(zip(Point._fields, p)))
older = ann._replace(age=ann.age + 1)
print(older.age, ann.age, older is ann, older == ann)
for attempt in [lambda: Point(1), lambda: Point(1, 2, 3), lambda: Point(1, 2, z=3), lambda: Point(1, x=2),
                lambda: Point(), lambda: Person("x")]:
    try:
        attempt()
    except TypeError as e:
        # (After the function's name, which isn't the same in every Python.)
        print("TypeError", str(e).split("() ", 1)[1])
for attempt in [lambda: namedtuple("Bad", "a b a"), lambda: namedtuple("Bad", "a class"), lambda: namedtuple("Bad", "a _b"),
                lambda: namedtuple("Bad", "a b-c"), lambda: namedtuple("Bad name", "a"), lambda: p._replace(z=1)]:
    try:
        attempt()
    except ValueError as e:
        print("ValueError", e)
try:
    Point._make([1, 2, 3])
except TypeError as e:
    print("TypeError", e)
try:
    namedtuple("Bad", "a", defaults=[1, 2])
except TypeError as e:
    print("TypeError", e)
try:
    p[5]
except IndexError as e:
    print("IndexError", e)


class Circle(namedtuple("Circle", "radius")):
    def area(self):
        return 3 * self.radius ** 2


print(Circle(2), Circle(2).area(), Circle(2).radius, Circle(1) == Circle(1))
Card = namedtuple("Card", "rank suit")
deck = [Card(rank, suit) for suit in "SH" for rank in "AK"]
print(deck[0], len(deck), [card.rank + card.suit for card in deck], sorted(deck)[0])

# ---- ChainMap ----
defaults = {"color": "red", "user": "guest"}
overrides = {"user": "ann"}
cm = ChainMap(overrides, defaults)
print(cm["user"], cm["color"], cm.get("size"), cm.get("size", "M"), len(cm), sorted(cm), "color" in cm, "size" in cm)
print(cm, list(cm), list(cm.keys()), list(cm.values()), list(cm.items()), dict(cm))
cm["size"] = "L"
print(overrides, defaults, cm["size"])
del cm["size"]
print(overrides, cm.maps)
child = cm.new_child({"color": "blue"})
print(child["color"], child["user"], child.parents["color"], child.parents == cm, len(child.maps))
print(ChainMap(), ChainMap({}).maps, bool(ChainMap()), bool(cm), ChainMap({"a": 1}) == {"a": 1})
try:
    cm["nope"]
except KeyError as e:
    print("KeyError", e)
try:
    del cm["color"]
except KeyError as e:
    print("KeyError", e)
print(cm.pop("user"), cm["user"], cm.new_child().maps[0], cm.setdefault("k", 1), overrides)
scopes = ChainMap({"x": 1})
inner = scopes.new_child()
inner["x"] = 2
inner["y"] = 3
print(inner["x"], scopes["x"], "y" in scopes, inner.parents["x"], list(inner))

# ---- classes of one's own made from them ----
class Tally(Counter):
    def top(self):
        return self.most_common(1)[0][0]


class Registry(defaultdict):
    pass


class History(deque):
    def latest(self):
        return self[-1]


class Settings(OrderedDict):
    pass


t = Tally("banana")
h = History([1, 2, 3], maxlen=5)
print(t, t.top(), t["n"], t.copy(), type(t.copy()).__name__, isinstance(t, Counter), Tally(), t + Tally("a"))
print(Registry(list), Registry(int, a=1), h, h.latest(), h.copy(), type(h.copy()).__name__, Settings(a=1), Settings())
print(Counter, defaultdict, OrderedDict, deque, ChainMap, type(t), type(Counter()), type(deque()))

# What the module has.
print(collections.Counter is Counter, [name for name in ["Counter", "defaultdict", "OrderedDict", "deque", "namedtuple", "ChainMap"] if not hasattr(collections, name)])
