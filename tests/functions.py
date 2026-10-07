# Functions, closures, lambdas, generators, recursion.
def add(a, b=10, *args, **kwargs):
    return a + b + sum(args) + sum(kwargs.values())

print(add(1), add(1, 2), add(1, 2, 3, 4), add(1, b=5), add(1, 2, 3, x=4, y=5))

def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(15)])

def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c = counter()
c()
c()
print(c(), counter()())

total = 0
def bump(n):
    global total
    total += n

bump(5)
bump(6)
print(total)

square = lambda x: x * x
print(square(7), (lambda a, b=2: a ** b)(3), list(map(lambda p: p[0] + p[1], [(1, 2), (3, 4)])))

def gen(n):
    for i in range(n):
        yield i * i

print(list(gen(5)), sum(gen(4)))
g = gen(3)
print(next(g), next(g), next(g), next(g, "done"))

def apply(f, *args, **kw):
    return f(*args, **kw)

print(apply(max, 3, 9, 4), apply(sorted, [3, 1, 2], reverse=True), apply(lambda **k: sorted(k), b=1, a=2))

def decorate(f):
    def wrapper(*args):
        return "<" + str(f(*args)) + ">"
    return wrapper

@decorate
def greet(name):
    return "hi " + name

print(greet("ana"), greet.__name__)

def defaults(a, b=[], c=None):
    b.append(a)
    return b

print(defaults(1), defaults(2), defaults(3, []))

def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

print(factorial(20), factorial(5))

def outer():
    x = "outer"
    def inner():
        return x
    x = "changed"
    return inner()

print(outer())
adders = [lambda x, n=n: x + n for n in range(3)]
print([f(10) for f in adders])
print((lambda: None)(), callable(print), callable(3))
def no_return():
    pass
print(no_return())
def kwonly(a, *, key=None):
    return (a, key)
print(kwonly(1, key="k"))
def walrus(xs):
    if (n := len(xs)) > 2:
        return n
    return 0
print(walrus([1, 2, 3]), walrus([]))
