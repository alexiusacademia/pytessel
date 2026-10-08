# The functools module: partial, lru_cache, cache, wraps, cmp_to_key,
# total_ordering, reduce.
#
# Author: Alexius Academia
# Date: 2026-10-08
import functools
from functools import partial, lru_cache, wraps, cmp_to_key, total_ordering, reduce, update_wrapper

# cache() came with Python 3.9.
cache = functools.cache

# ---- reduce ----
print(reduce(lambda a, b: a + b, [1, 2, 3, 4]))
print(reduce(lambda a, b: a * b, range(1, 6), 1))
print(reduce(lambda a, b: a + b, [], "start"))
print(reduce(max, [3, 9, 2]))
print(reduce(lambda acc, w: acc + [len(w)], ["a", "bb", "ccc"], []))
try:
    reduce(lambda a, b: a + b, [])
except TypeError as e:
    print("TypeError")

# ---- partial ----
def power(base, exponent):
    return base ** exponent


square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(square(5), cube(2), square(base=7))
two_to = partial(power, 2)
print(two_to(10), [two_to(n) for n in range(5)])
print(two_to.func is power, two_to.args, two_to.keywords, square.args, square.keywords)


def greet(greeting, name, punctuation="!"):
    return greeting + ", " + name + punctuation


hello = partial(greet, "Hello")
print(hello("Ann"), hello("Bob", punctuation="?"), hello("Cy", "."))
polite = partial(hello, punctuation=".")
print(polite("Dee"), polite.func is greet, polite.args, polite.keywords)
print(polite("Eve", punctuation="…"))
print(list(map(partial(max, 5), [1, 7, 3, 9])))
print(sorted(["b", "A", "c"], key=partial(str.lower)))
binary = partial(int, "1010")
print(binary(2), binary(8), partial(round, 3.14159)(2))
print(partial(sorted, reverse=True)([3, 1, 2]))
print(callable(square), partial(lambda *a, **k: (a, k), 1, 2, x=3)(4, y=5))
join = partial("-".join)
print(join(["a", "b"]))
try:
    partial(5)
except TypeError as e:
    print("TypeError", e)
try:
    partial()
except TypeError as e:
    print("TypeError")
try:
    square(1, 2)
except TypeError as e:
    print("TypeError", e)

# ---- lru_cache ----
calls = []


@lru_cache(maxsize=None)
def fib(n):
    calls.append(n)
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(30), len(calls), fib(30), len(calls))
print(fib.cache_info())
print(fib.__name__, fib.__wrapped__(3))
fib.cache_clear()
print(fib.cache_info())
print(fib(10), fib.cache_info())


@lru_cache
def double(x):
    calls.append(("double", x))
    return x * 2


del calls[:]
print(double(2), double(2), double(3), double(2), calls)
print(double.cache_info(), double.__name__)
print(double.cache_parameters())


@lru_cache()
def triple(x):
    return x * 3


print(triple(1), triple(1), triple.cache_info())


@lru_cache(maxsize=2)
def slow(x):
    calls.append(x)
    return x * 10


del calls[:]
print(slow(1), slow(2), slow(1), slow(3), slow(2), slow(1))
print(calls, slow.cache_info())
info = slow.cache_info()
print(info.hits, info.misses, info.maxsize, info.currsize)


@lru_cache(maxsize=0)
def never(x):
    calls.append(x)
    return x


del calls[:]
print(never(1), never(1), calls, never.cache_info())


@lru_cache(maxsize=8)
def keyed(a, b=2, *rest, **more):
    calls.append((a, b, rest, sorted(more.items())))
    return a + b


del calls[:]
print(keyed(1), keyed(1), keyed(1, 2), keyed(1, b=2), keyed(a=1, b=2), keyed(1, 2, 3), keyed(1, x=5), keyed(1, x=5))
print(len(calls), keyed.cache_info())


@lru_cache(maxsize=None, typed=True)
def typed(x):
    calls.append(x)
    return x


del calls[:]
print(typed(1), typed(1.0), typed(1), calls, typed.cache_info())
try:
    double([1, 2])
except TypeError as e:
    print("TypeError", e)
try:
    lru_cache("big")
except TypeError as e:
    print("TypeError", e)


@cache
def factorial(n):
    return n * factorial(n - 1) if n else 1


print(factorial(10), factorial(12), factorial.cache_info())


class Shape:
    def __init__(self, side):
        self.side = side

    @lru_cache(maxsize=None)
    def area(self):
        calls.append("area")
        return self.side ** 2


del calls[:]
s = Shape(4)
print(s.area(), s.area(), Shape(5).area(), calls)


@lru_cache(maxsize=None)
def collatz(n):
    if n == 1:
        return 0
    return 1 + collatz(n // 2 if n % 2 == 0 else 3 * n + 1)


print(max(range(1, 200), key=collatz), collatz(27))

# ---- wraps ----
def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        calls.append(func.__name__)
        return func(*args, **kwargs)
    return wrapper


@logged
def add(a, b=1):
    """Adds two numbers."""
    return a + b


del calls[:]
print(add(1), add(2, b=3), add.__name__, calls, add.__wrapped__.__name__, add.__wrapped__(5, 5))


def plain(func):
    def wrapper(*args):
        return func(*args)
    return wrapper


@plain
def sub(a, b):
    return a - b


print(sub.__name__, sub(5, 3))


def tagged(tag):
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            return "<%s>%s</%s>" % (tag, func(*args), tag)
        return wrapper
    return decorator


@tagged("b")
@tagged("i")
def text(s):
    return s


print(text("hi"), text.__name__, text.__wrapped__.__name__, text.__wrapped__.__wrapped__("x"))


def marked(func):
    func.marked = True
    func.note = "seen"
    return func


@logged
@marked
def noted():
    return 1


print(noted.marked, noted.note, noted.__name__, noted())
w = update_wrapper(lambda: 0, add)
print(w.__name__, w(), w.__wrapped__ is add)


def counted(func):
    @wraps(func)
    def wrapper(*args):
        wrapper.count += 1
        return func(*args)
    wrapper.count = 0
    return wrapper


@counted
def ping():
    return "pong"


print(ping(), ping(), ping.count, ping.__name__)

# ---- cmp_to_key ----
def by_length_then_text(a, b):
    if len(a) != len(b):
        return len(a) - len(b)
    return (a > b) - (a < b)


words = ["pear", "fig", "apple", "kiwi", "date", "plum", "banana"]
print(sorted(words, key=cmp_to_key(by_length_then_text)))
print(sorted(words, key=cmp_to_key(by_length_then_text), reverse=True))
print(sorted([3, 1, 2], key=cmp_to_key(lambda a, b: b - a)))
print(max(words, key=cmp_to_key(by_length_then_text)), min(words, key=cmp_to_key(by_length_then_text)))
numbers = [5, 2, 9, 1]
numbers.sort(key=cmp_to_key(lambda a, b: a - b))
print(numbers)
K = cmp_to_key(lambda a, b: a - b)
print(K(1) < K(2), K(2) < K(1), K(1) == K(1), K(1) <= K(1), K(2) > K(1), K(1) >= K(2), K(3).obj)
print(sorted(["10", "9", "100", "1"], key=cmp_to_key(lambda a, b: int(a) - int(b))))


def version_compare(a, b):
    pa = [int(x) for x in a.split(".")]
    pb = [int(x) for x in b.split(".")]
    return (pa > pb) - (pa < pb)


print(sorted(["1.10", "1.2", "1.9.1", "1.9"], key=cmp_to_key(version_compare)))

# ---- total_ordering ----
@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)

    def __repr__(self):
        return "v%d.%d" % (self.major, self.minor)


a, b, c = Version(1, 2), Version(1, 10), Version(1, 2)
print(a < b, a <= b, a > b, a >= b, a == c, a != b, a <= c, a >= c, b > a, b >= a)
print(sorted([b, a, Version(0, 9)]), max(a, b), min(a, b))


@total_ordering
class Grade:
    def __init__(self, score):
        self.score = score

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score > other.score


print(Grade(1) < Grade(2), Grade(2) <= Grade(2), Grade(3) >= Grade(2), Grade(1) > Grade(2), Grade(2) < Grade(1))


@total_ordering
class Size:
    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        return self.n == other.n

    def __le__(self, other):
        return self.n <= other.n


print(Size(1) < Size(2), Size(2) < Size(2), Size(3) > Size(2), Size(2) >= Size(2), Size(1) >= Size(2))


@total_ordering
class Rank:
    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        return self.n == other.n

    def __ge__(self, other):
        return self.n >= other.n


print(Rank(1) < Rank(2), Rank(2) <= Rank(2), Rank(3) > Rank(2), Rank(2) > Rank(2), Rank(1) <= Rank(0))
try:
    @total_ordering
    class Nothing:
        pass
except ValueError as e:
    print("ValueError", e)
