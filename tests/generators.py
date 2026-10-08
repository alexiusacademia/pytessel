# Generators and lazy iterators: a value at a time.

# ---- a generator runs up to each yield, when it's asked ----
def three():
    print("  start")
    yield 1
    print("  after 1")
    yield 2
    print("  after 2")
    yield 3
    print("  end")

g = three()
print("made", type(g).__name__)
print(next(g))
print("between")
print(next(g))
print(next(g))
try:
    next(g)
except StopIteration as e:
    print("stopped", e.value)
# Once done, it's done for good.
for again in range(2):
    try:
        next(g)
    except StopIteration:
        print("still stopped")
print(next(g, "default"))
print(list(g))

for x in three():
    print("got", x)

# ---- generators that never end ----
def count(start=0, step=1):
    n = start
    while True:
        yield n
        n += step

def take(n, iterable):
    out = []
    for x in iterable:
        if len(out) == n:
            break
        out.append(x)
    return out

def islice(iterable, n):
    it = iter(iterable)
    for _ in range(n):
        try:
            yield next(it)
        except StopIteration:
            return

c = count()
print(next(c), next(c), next(c))
print(take(5, count(10, 5)))
print(list(islice(count(), 4)))
for n in count(1):
    if n * n > 50:
        print("first square over 50:", n * n)
        break
print(list(zip(count(), "abc")))
print(list(zip("ab", count(100), count(0, -1))))

def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print(take(12, fib()))
print(next(x for x in fib() if x > 1000))

# ---- return value, StopIteration.value ----
def returns():
    yield 1
    return "result"

r = returns()
print(next(r))
try:
    next(r)
except StopIteration as e:
    print("value:", e.value, e.args)

def nothing():
    return 5
    yield

n = nothing()
try:
    next(n)
except StopIteration as e:
    print("value:", e.value)
print(list(nothing()))
try:
    raise StopIteration("mine", 2)
except StopIteration as e:
    print(e.value, e.args)
try:
    raise StopIteration
except StopIteration as e:
    print(e.value, e.args)

# ---- yield inside if / while / for / nested loops, with break, continue ----
def branches(n):
    if n < 0:
        yield "negative"
    elif n == 0:
        yield "zero"
    else:
        yield "positive"
        if n > 10:
            yield "big"
    yield "done"

for n in (-1, 0, 5, 50):
    print(list(branches(n)))

def loops():
    for i in range(5):
        if i == 1:
            continue
        if i == 4:
            break
        for j in range(3):
            if j == 2:
                break
            yield (i, j)
        else:
            yield "never"
    else:
        yield "not here"
    k = 0
    while k < 10:
        k += 1
        if k % 2:
            continue
        yield k
        if k == 6:
            break
    else:
        yield "no"
    while k < 8:
        k += 1
        yield k
    else:
        yield "while else"
    for z in []:
        yield z
    else:
        yield "for else"

print(list(loops()))

def early(xs):
    for x in xs:
        if x < 0:
            return "negative found"
        yield x
    return "all fine"

def run(g):
    out = []
    while True:
        try:
            out.append(next(g))
        except StopIteration as e:
            return out, e.value

print(run(early([1, 2, 3])))
print(run(early([1, -2, 3])))

# A loop over another generator, and over a list that grows.
def doubled(g):
    for x in g:
        yield x * 2

print(take(5, doubled(doubled(count(1)))))

def growing():
    xs = [1]
    for x in xs:
        if x < 5:
            xs.append(x + 1)
        yield x

print(list(growing()))

# ---- side effects happen in turn ----
def producer():
    for i in range(3):
        print("  producing", i)
        yield i

for v in producer():
    print("  consuming", v)

# ---- send ----
def averager():
    total = 0
    count = 0
    average = None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

a = averager()
print(next(a))
print(a.send(10), a.send(20), a.send(60))

def echo():
    received = yield "ready"
    while received != "stop":
        received = yield "got " + str(received)
    return "bye"

e = echo()
print(e.send(None))
print(e.send("a"))
print(next(e))
try:
    e.send("stop")
except StopIteration as stop:
    print("ended:", stop.value)

try:
    echo().send(1)
except TypeError as err:
    print("TypeError:", err)

def bare():
    x = yield
    print("  x =", x)
    y = z = yield
    print("  y, z =", y, z)
    a, b = yield "pair"
    print("  a, b =", a, b)
    total = 100
    total += yield "add"
    print("  total =", total)
    d = {"k": 1}
    d["k"] += yield "item"
    print("  d =", d)
    return (yield "last")

b = bare()
print(next(b))
print(b.send(1))
print(b.send(2))
print(b.send((3, 4)))
print(b.send(5))
print(b.send(6))
try:
    b.send("the end")
except StopIteration as stop:
    print("returned", stop.value)

class Box:
    pass

def into_attribute(box):
    box.value = yield "first"
    box.value += yield "second"

box = Box()
ia = into_attribute(box)
next(ia)
ia.send(10)
try:
    ia.send(5)
except StopIteration:
    pass
print(box.value)

# ---- throw ----
def catcher():
    while True:
        try:
            x = yield "waiting"
            print("  got", x)
        except ValueError as err:
            print("  caught", err)
            yield "recovered"
        except KeyError:
            print("  key error, leaving")
            return "left"

ct = catcher()
print(next(ct))
print(ct.throw(ValueError("bad")))
print(next(ct))
print(ct.send(1))
print(ct.throw(ValueError, "worse"))
print(next(ct))
try:
    ct.throw(KeyError)
except StopIteration as stop:
    print("stop:", stop.value)
try:
    ct.throw(TypeError("after the end"))
except TypeError as err:
    print("TypeError:", err)

def simple():
    yield 1
    yield 2

s = simple()
next(s)
try:
    s.throw(RuntimeError("out"))
except RuntimeError as err:
    print("RuntimeError:", err)
print(list(s))
s = simple()
try:
    s.throw(RuntimeError("before start"))
except RuntimeError as err:
    print("RuntimeError:", err)
print(list(s))

# ---- close, try/finally ----
def guarded(name):
    print("  open", name)
    try:
        yield 1
        yield 2
    finally:
        print("  close", name)

gd = guarded("a")
print(next(gd))
gd.close()
gd.close()
print(list(gd))
gd = guarded("b")
gd.close()
print(list(gd))
print(list(guarded("c")))

# A loop left early closes the generator it was given (nothing else has it).
def first_of(name):
    for x in guarded(name):
        return x

for x in guarded("d"):
    print("  breaking")
    break
print("after the loop")
print(first_of("e"))

def passes_on(name):
    for x in guarded(name):
        yield x * 10
    print("  not reached")

for x in passes_on("f"):
    break
po = passes_on("g")
print(next(po))
po.close()
kept = guarded("h")
for x in kept:
    break
print("still open:", next(kept))
kept.close()

def sees_exit():
    try:
        yield 1
    except GeneratorExit:
        print("  GeneratorExit seen")
        raise

se = sees_exit()
next(se)
print(se.close())

stubbornness = [True]

def stubborn():
    while stubbornness[0]:
        try:
            yield "no"
        except GeneratorExit:
            pass

sb = stubborn()
next(sb)
try:
    sb.close()
except RuntimeError as err:
    print("RuntimeError:", err)
stubbornness[0] = False
print(sb.close(), list(sb))

def closing_returns():
    try:
        yield 1
    except GeneratorExit:
        return "ignored"

cr = closing_returns()
next(cr)
print(cr.close())

def tries():
    try:
        yield "in try"
        raise ValueError("oops")
    except ValueError as err:
        yield "in except: " + str(err)
        try:
            raise
        except ValueError:
            yield "raised again"
    else:
        yield "not reached"
    finally:
        yield "in finally"
    try:
        yield "second try"
    except ValueError:
        yield "not reached"
    else:
        yield "in else"
    finally:
        print("  finally with no yield")
    for i in range(3):
        try:
            if i == 1:
                continue
            if i == 2:
                break
            yield i
        finally:
            yield "finally %d" % i
    try:
        return "returned"
    finally:
        yield "finally before return"

print(run(tries()))

def raises_in_finally():
    try:
        yield 1
        raise KeyError("first")
    finally:
        yield "cleanup"
        print("  cleanup done")

rf = raises_in_finally()
print(next(rf), next(rf))
try:
    next(rf)
except KeyError as err:
    print("KeyError:", err)

def nested_finally():
    try:
        try:
            yield 1
        finally:
            print("  inner finally")
            yield 2
    finally:
        print("  outer finally")

nf = nested_finally()
print(next(nf))
print(nf.throw(ValueError("x")))
try:
    next(nf)
except ValueError as err:
    print("ValueError:", err)

def handling():
    try:
        raise ValueError("kept")
    except ValueError:
        yield 1
        try:
            raise
        except ValueError as err:
            yield "still " + str(err)

h = handling()
print(next(h))
try:
    raise KeyError("other")
except KeyError:
    print(next(h))

# An exception inside, seen by the one who asked.
def breaks():
    yield 1
    raise ValueError("broken")

bk = breaks()
print(next(bk))
try:
    next(bk)
except ValueError as err:
    print("ValueError:", err)
print(list(bk))

def stops():
    yield 1
    raise StopIteration("inside")

try:
    list(stops())
except RuntimeError as err:
    print("RuntimeError:", err)

def reenters():
    yield next(me)

me = reenters()
try:
    next(me)
except ValueError as err:
    print("ValueError:", err)

# ---- with ----
class Managed:
    def __init__(self, name, swallow=False):
        self.name = name
        self.swallow = swallow
    def __enter__(self):
        print("  enter", self.name)
        return self.name
    def __exit__(self, kind, value, trace):
        print("  exit", self.name, kind.__name__ if kind else None)
        return self.swallow

def managed():
    with Managed("a") as a:
        yield a
        with Managed("b") as b, Managed("c") as c:
            yield b + c
        yield "after inner"
    with Managed("d", swallow=True):
        yield "in d"
        raise ValueError("swallowed")
    yield "after d"
    with Managed("e"):
        return "from with"

print(run(managed()))
m = managed()
print(next(m))
m.close()
m = managed()
next(m)
print(next(m))
try:
    m.throw(KeyError("k"))
except KeyError:
    print("KeyError came out")

# ---- yield from ----
def inner():
    x = yield "inner 1"
    print("  inner got", x)
    y = yield "inner 2"
    print("  inner got", y)
    return "inner result"

def outer():
    print("  outer start")
    result = yield from inner()
    print("  result:", result)
    yield from [10, 20]
    yield from "ab"
    yield from range(2)
    yield from (i * i for i in range(3))
    again = yield from inner()
    return again.upper()

o = outer()
print(next(o))
print(o.send("A"))
print(o.send("B"))
print(run(o))

def chain(*iterables):
    for it in iterables:
        yield from it

print(list(chain([1, 2], (3,), "45", range(6, 8), chain([8], [9]))))

def through():
    try:
        yield from catcher()
    finally:
        print("  through done")

t = through()
print(next(t))
print(t.throw(ValueError("passed in")))
print(next(t))
try:
    t.throw(KeyError)
except StopIteration:
    print("through ended")

t = through()
next(t)
t.close()

def delegating_close():
    yield from guarded("inside")

dc = delegating_close()
print(next(dc))
dc.close()

def returns_from():
    return (yield from returns())

print(run(returns_from()))

def empty_from():
    x = yield from []
    yield x

print(list(empty_from()))

class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.n == 0:
            raise StopIteration("liftoff")
        self.n -= 1
        return self.n + 1

def from_object():
    word = yield from Countdown(3)
    yield word

print(list(from_object()))

# A tree, walked by a generator that calls itself.
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def insert(node, value):
    if node is None:
        return Node(value)
    if value < node.value:
        node.left = insert(node.left, value)
    else:
        node.right = insert(node.right, value)
    return node

def walk(node):
    if node is not None:
        yield from walk(node.left)
        yield node.value
        yield from walk(node.right)

def depth_first(node, depth=0):
    if node is None:
        return 0
    left = yield from depth_first(node.left, depth + 1)
    yield (node.value, depth)
    right = yield from depth_first(node.right, depth + 1)
    return left + right + 1

root = None
for v in [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]:
    root = insert(root, v)
print(list(walk(root)))
print(run(depth_first(root)))
print(next(walk(root)))

def flatten(xs):
    for x in xs:
        if isinstance(x, list):
            yield from flatten(x)
        else:
            yield x

print(list(flatten([1, [2, [3, [4, [5]]], 6], [[7]], 8])))

def permutations(items):
    if len(items) <= 1:
        yield list(items)
        return
    for i in range(len(items)):
        for rest in permutations(items[:i] + items[i + 1:]):
            yield [items[i]] + rest

print(take(4, permutations([1, 2, 3, 4])))
print(len(list(permutations("abcd"))))

# ---- generator expressions ----
def noisy(x):
    print("  noisy", x)
    return x

ge = (noisy(x) * 10 for x in range(5) if x % 2 == 0)
print("made", type(ge).__name__)
print(next(ge))
print(next(ge))
print(list(ge))
print(list(ge))
print(next((x for x in count() if x > 3)))
pairs = ((a, b) for a in count() for b in range(a) if (a + b) % 3 == 0)
print(take(5, pairs))
k = 2
scaled = (x * k for x in range(3))
k = 10
print(list(scaled))
def make():
    factor = 3
    return (x * factor for x in count())
print(take(3, make()))
print(sum(x * x for x in range(10)), max(len(w) for w in ["a", "bcd", "ef"]))
print(",".join(str(x) for x in range(5)))
print(sorted(x % 3 for x in range(7)))
print(dict((x, x * x) for x in range(4)))
print(set(x // 2 for x in range(6)) == {0, 1, 2})
print(tuple(x for x in "abc"))
try:
    (x for x in 5)
except TypeError as err:
    print("TypeError:", err)
gx = (1 / x for x in [1, 0, 2])
print(next(gx))
try:
    next(gx)
except ZeroDivisionError as err:
    print("ZeroDivisionError:", err)
print(list(gx))
gx = (x for x in range(3))
gx.close()
print(list(gx))
print(gx is iter(gx), g is iter(g))

# ---- map, filter, zip, enumerate take a value when asked ----
def numbers():
    n = 0
    while True:
        n += 1
        print("  number", n)
        yield n

def square(x):
    print("  square", x)
    return x * x

def odd(x):
    print("  odd?", x)
    return x % 2 == 1

m = map(square, numbers())
print("map made")
print(next(m))
print(next(m))
f = filter(odd, numbers())
print("filter made")
print(next(f))
print(next(f))
z = zip(numbers(), "ab")
print("zip made")
print(list(z))
en = enumerate(numbers(), 10)
print("enumerate made")
print(next(en), next(en))
print(take(3, map(lambda a, b: a + b, count(), count(100))))
print(take(3, filter(None, count())))
print(take(3, enumerate(count(5))))
print(take(2, zip(count(), count(1), count(2))))
print(next(map(str, count(7))))
print(list(map(lambda x: x + 1, [1, 2, 3])), list(filter(lambda x: x > 1, (1, 2, 3))))
print(list(zip()), list(zip([1, 2], "abc", range(5))))
print(list(enumerate("ab")), list(enumerate("ab", start=1)))
print([type(v).__name__ for v in (map(str, []), filter(None, []), zip(), enumerate([]))])
mm = map(str, [1, 2])
print(mm is iter(mm), list(mm), list(mm))

# A pipeline of generators: each value goes all the way through first.
def read(lines):
    for line in lines:
        print("  read", repr(line))
        yield line

def strip(lines):
    for line in lines:
        yield line.strip()

def non_empty(lines):
    for line in lines:
        if line:
            yield line
        else:
            print("  skipped an empty line")

def numbered(lines):
    for i, line in enumerate(lines, 1):
        yield "%d: %s" % (i, line)

for line in numbered(non_empty(strip(read([" a ", "", "b\n", "   ", "c"])))):
    print(line)

pipeline = map(lambda x: x * 3, filter(lambda x: x % 2, (x + 1 for x in doubled(count()))))
print(take(4, pipeline))

# ---- any, all, in stop early ----
def watched(xs):
    for x in xs:
        print("  looked at", x)
        yield x

print(any(x > 1 for x in watched([0, 1, 2, 3, 4])))
print(all(x < 2 for x in watched([0, 1, 2, 3, 4])))
print(any(watched([])), all(watched([])))
print(any(x > 10 for x in count()), all(x < 10 for x in count()))
print(3 in watched([1, 2, 3, 4, 5]))
print(9 in watched([1, 2]))
print(25 in (x * x for x in count()))
w = watched([1, 2, 3, 4])
print(2 in w, list(w))

# ---- unpacking, splats, the other consumers ----
a, b, c = (x * 2 for x in range(3))
print(a, b, c)
first, *rest = (x for x in range(5))
print(first, rest)
try:
    a, b = count()
except ValueError as err:
    print("ValueError:", err)
try:
    a, b, c = (x for x in range(2))
except ValueError as err:
    print("ValueError:", err)
def show(*args):
    print(args)
show(*(x for x in "xyz"))
print([*map(str, range(3)), *zip("a", "b")])
print(list(reversed([1, 2, 3])), list(reversed(range(5))), list(reversed("abc")), list(reversed(range(0, 10, 3))))
print(min(x for x in [3, 1, 2]), max(map(abs, [-5, 2])), sum(map(int, "123")), sum((x for x in [1.5, 2.5]), 10))
print(sorted(filter(None, [3, 0, 1])), len(list(zip(range(1000000000000), "ab"))))
print(dict(zip("abc", count())), dict(enumerate("xy")))
xs = []
xs.extend(x for x in range(3))
xs += (x for x in range(3, 5))
print(xs, [x for x in iter(xs)], {x for x in map(abs, [-1, 1])}, {k: v for k, v in zip("ab", count())})

# ---- iter and next ----
it = iter([1, 2, 3])
print(next(it), next(it), next(it), next(it, "none left"))
lst = [1, 2]
it = iter(lst)
print(next(it))
lst.append(3)
print(list(it))
lst.append(4)
print(list(it))
it = iter(range(10 ** 12))
print(next(it), next(it))
it = iter("hi")
print(next(it), next(it), next(it, None))
it = iter({"a": 1, "b": 2})
print(next(it), list(it))
it = iter((1, 2))
print(it is iter(it), list(it))
calls = []
def countdown():
    calls.append(len(calls))
    return 3 - len(calls)
print(list(iter(countdown, 0)), calls)
readings = iter([5, 6, -1, 7])
print(list(iter(lambda: next(readings), -1)), list(readings))
try:
    iter(5)
except TypeError as err:
    print("TypeError:", err)
try:
    next([1, 2])
except TypeError as err:
    print("TypeError:", err)
try:
    for x in 5:
        pass
except TypeError as err:
    print("TypeError:", err)
print(g.__next__ is not None, next(iter(three.__name__)))
nx = count().__next__
print(nx(), nx(), nx())
print(next(iter(range(0)), "empty range"))

# ---- classes: iterators of their own, and generators as methods ----
class Evens:
    """An iterator class: never ends."""
    def __init__(self):
        self.n = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.n += 2
        return self.n

print(take(3, Evens()), take(2, zip(Evens(), count())), next(map(str, Evens())))
print(take(3, (x + 1 for x in Evens())), take(2, enumerate(Evens())), 8 in Evens())
print(take(2, filter(lambda x: x % 4 == 0, Evens())))
a, b = Countdown(2)
print(a, b, list(Countdown(3)), sum(Countdown(4)), list(doubled(Countdown(2))))
try:
    a, b = Evens()
except ValueError as err:
    print("ValueError:", err)

class Bag:
    def __init__(self, *items):
        self.items = list(items)
    def __iter__(self):
        for item in self.items:
            yield item
    def pairs(self):
        for i, item in enumerate(self.items):
            yield i, item
    def forever(self):
        while True:
            yield from self
    @staticmethod
    def static(n):
        yield from range(n)
    @classmethod
    def named(cls):
        yield cls.__name__

bag = Bag("x", "y", "z")
print(list(bag), list(bag), list(bag.pairs()), take(7, bag.forever()))
print([a + b for a in bag for b in bag if a != b])
print(list(Bag.static(3)), list(bag.static(2)), list(Bag.named()), "y" in bag, "q" in bag)
x, y, z = bag
print(x, y, z, sorted(bag, reverse=True), max(bag), dict(bag.pairs()), "-".join(bag))

class Base:
    def items(self):
        yield "base"

class Derived(Base):
    def items(self):
        yield "derived"
        yield from super().items()

print(list(Derived().items()))

class OldStyle:
    def __getitem__(self, i):
        if i >= 3:
            raise IndexError
        return i * 10

print(list(OldStyle()), next(iter(OldStyle())), [x for x in OldStyle()], 20 in OldStyle())

class NotAnIterator:
    def __iter__(self):
        return [1, 2]

try:
    list(NotAnIterator())
except TypeError as err:
    print("TypeError:", err)

# ---- closures and several generators at once ----
def counter_pair():
    total = 0
    def add(n):
        nonlocal total
        while True:
            total += n
            yield total
    return add(1), add(10)

one, ten = counter_pair()
print(next(one), next(ten), next(one), next(ten), next(one))

def sieve():
    def filtered(numbers, prime):
        for n in numbers:
            if n % prime:
                yield n
    numbers = count(2)
    while True:
        prime = next(numbers)
        yield prime
        numbers = filtered(numbers, prime)

print(take(15, sieve()))

gens = [count(i * 100) for i in range(3)]
print([next(g2) for g2 in gens], [next(g2) for g2 in gens])

def with_local_function():
    def helper(x):
        return x * 2
    for i in range(3):
        yield helper(i)
    square = lambda v: v * v
    yield square(7)
    yield [helper(q) for q in range(3)]

print(list(with_local_function()))

def uses_global():
    global tally
    for i in range(3):
        tally += i
        yield tally

tally = 100
print(list(uses_global()), tally)

def default_args(a, b=2, *args, **kwargs):
    yield a
    yield b
    yield args
    yield sorted(kwargs.items())

print(list(default_args(1)), list(default_args(1, 3, 4, 5, k=6)))
try:
    default_args()
except TypeError as err:
    print("TypeError:", err)

def decorated(function):
    def wrapper(*args):
        return list(function(*args))
    return wrapper

@decorated
def letters(word):
    for letter in word:
        yield letter.upper()

print(letters("abc"))

# Deep, but not too deep: a chain of generators.
def countdown_from(n):
    if n > 0:
        yield n
        yield from countdown_from(n - 1)

print(sum(countdown_from(100)))
link = count()
for _ in range(50):
    link = doubled(link)
print(take(2, link))
