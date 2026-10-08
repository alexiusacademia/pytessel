# Descriptors, __slots__, and the hooks on attribute access.


def attempt(f, *args):
    try:
        print(f(*args))
    except Exception as e:
        print(type(e).__name__ + ":", e)


# ---- a data descriptor: __get__, __set__, __delete__, __set_name__ ----
class Typed:
    def __init__(self, kind):
        self.kind = kind

    def __set_name__(self, owner, name):
        self.name = name
        self.slot = "_" + name
        self.owner = owner.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.slot, "unset")

    def __set__(self, obj, value):
        if not isinstance(value, self.kind):
            raise TypeError("%s.%s must be %s, not %s" % (self.owner, self.name, self.kind.__name__, type(value).__name__))
        setattr(obj, self.slot, value)

    def __delete__(self, obj):
        print("deleting", self.name)
        delattr(obj, self.slot)


class Person:
    name = Typed(str)
    age = Typed(int)

    def __init__(self, name, age):
        self.name = name
        self.age = age


p = Person("Ada", 36)
print(p.name, p.age, sorted(p.__dict__.items()))
p.age = 37
p.age += 1
print(p.age, p._age)


def set_bad():
    p.age = "old"


attempt(set_bad)
attempt(lambda: Person(5, 5))
print(type(Person.name).__name__, Person.name.name, Person.age.slot, Person.name.owner)
del p.age
print(p.age)
q = Person("Bob", 1)
print(q.name, p.name, q.age, p.age)
# A data descriptor comes before what the object itself has.
p.__dict__["name"] = "in the dict"
print(p.name)
print(getattr(p, "name"), hasattr(p, "age"), hasattr(p, "nothing"))
setattr(p, "name", "Eve")
print(p.name)


# ---- a non-data descriptor: only __get__; the object's own attribute wins ----
class Lazy:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return "Lazy on the class"
        print("computing", self.name)
        value = self.function(obj)
        obj.__dict__[self.name] = value
        setattr(obj, self.name, value)
        return value


class Circle:
    def __init__(self, r):
        self.r = r

    @Lazy
    def area(self):
        return 3 * self.r * self.r


c = Circle(2)
print(c.area)
print(c.area)
print(Circle.area, Circle(1).area)
c.area = "overwritten"
print(c.area)
del c.area
print(c.area)


class Const:
    def __get__(self, obj, objtype=None):
        return ("const", obj is None, objtype.__name__)


class Holder:
    k = Const()


h = Holder()
print(h.k, Holder.k)
h.k = "own"
print(h.k, Holder.k)


class Sub(Holder):
    pass


print(Sub().k, Sub.k)


# ---- read-only and write-only descriptors ----
class ReadOnly:
    def __get__(self, obj, objtype=None):
        return 42

    def __set__(self, obj, value):
        raise AttributeError("can't set this")


class OnlyDelete:
    def __delete__(self, obj):
        print("__delete__ called")


class Guarded:
    answer = ReadOnly()
    gone = OnlyDelete()


g = Guarded()
print(g.answer)


def write_answer():
    g.answer = 1


attempt(write_answer)


def write_gone():
    g.gone = 1


attempt(write_gone)
del g.gone
print(type(g.gone).__name__)


# ---- a method is a descriptor; functions set on a class afterwards too ----
class Late:
    pass


def greet(self):
    return "hello from " + type(self).__name__


Late.greet = greet
Late.number = Typed(int)
Late.number.__set_name__(Late, "number")
late = Late()
late.number = 5
print(late.greet(), late.number, late._number)


# ---- property, on the same footing ----
class Temperature:
    def __init__(self):
        self._c = 0

    @property
    def celsius(self):
        return self._c

    @celsius.setter
    def celsius(self, value):
        if value < -273:
            raise ValueError("too cold")
        self._c = value

    @celsius.deleter
    def celsius(self):
        print("deleter runs")
        self._c = None

    @property
    def fahrenheit(self):
        return self._c * 9 / 5 + 32

    def get_k(self):
        return self._c + 273

    def set_k(self, value):
        self._c = value - 273

    kelvin = property(get_k, set_k)


t = Temperature()
t.celsius = 100
print(t.celsius, t.fahrenheit, t.kelvin)
t.kelvin = 0
print(t.celsius)


def too_cold():
    t.celsius = -300


attempt(too_cold)


def no_setter():
    t.fahrenheit = 1


attempt(no_setter)


def no_deleter():
    del t.fahrenheit


attempt(no_deleter)
del t.celsius
print(t.celsius, type(Temperature.celsius).__name__, Temperature.celsius.fget is not None)
t.__dict__["celsius"] = "shadow"
t._c = 1
print(t.celsius)


# ---- __slots__ ----
class P:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def total(self):
        return self.x + self.y


s = P(1, 2)
s.x = 10
print(s.x, s.y, s.total())


def set_z():
    s.z = 3


attempt(set_z)
attempt(lambda: s.__dict__)
attempt(lambda: s.z)
del s.y
attempt(lambda: s.y)
s.y = 5
print(s.y, hasattr(s, "x"), hasattr(s, "z"), hasattr(s, "__dict__"), P.__slots__)


class P3(P):
    __slots__ = ["z"]


s3 = P3(1, 2)
s3.z = 3
print(s3.x, s3.y, s3.z)


def set_w():
    s3.w = 4


attempt(set_w)


class Loose(P):
    pass


loose = Loose(1, 2)
loose.anything = "fine"
print(loose.anything, loose.__dict__, loose.x)


class One:
    __slots__ = "only"


one = One()
one.only = 1


def set_other():
    one.other = 2


attempt(set_other)
print(one.only)


class WithClassAttr:
    __slots__ = ("a",)
    shared = "class level"


w = WithClassAttr()
print(w.shared)


def set_shared():
    w.shared = "mine"


attempt(set_shared)


class Empty:
    __slots__ = ()


def set_any():
    Empty().a = 1


attempt(set_any)


# ---- __getattr__, __getattribute__, __setattr__, __delattr__ ----
class Fallback:
    def __init__(self):
        self.real = "real"

    def __getattr__(self, name):
        if name.startswith("x"):
            return "made up " + name
        raise AttributeError("no " + name)


f = Fallback()
print(f.real, f.x1, getattr(f, "xyz"), getattr(f, "other", "default"), hasattr(f, "x"), hasattr(f, "y"))
attempt(lambda: f.other)


class Logged:
    def __init__(self):
        self.log = []
        self.value = 1

    def __getattribute__(self, name):
        if name != "log":
            object.__getattribute__(self, "log").append(name)
        return object.__getattribute__(self, name)

    def method(self):
        return self.value * 2


lg = Logged()
print(lg.value, lg.method(), lg.log)
attempt(lambda: lg.missing)


class Upper:
    def __getattribute__(self, name):
        if name.isupper():
            return name.lower()
        return super().__getattribute__(name)

    def __getattr__(self, name):
        return "fallback for " + name

    plain = "plain"


u = Upper()
print(u.ABC, u.plain, u.other)


class Validated:
    def __init__(self):
        self.count = 0
        self.name = "n"

    def __setattr__(self, name, value):
        if name == "count" and value < 0:
            raise ValueError("count can't be negative")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name == "name":
            raise AttributeError("name stays")
        super().__delattr__(name)


v = Validated()
v.count = 5
v.extra = "x"
print(v.count, v.extra, sorted(v.__dict__))


def negative():
    v.count = -1


attempt(negative)


def delete_name():
    del v.name


attempt(delete_name)
del v.extra
attempt(lambda: v.extra)
setattr(v, "count", 9)
attempt(lambda: setattr(v, "count", -9))
print(v.count)


class Frozen:
    def __init__(self, **values):
        for key, value in values.items():
            super().__setattr__(key, value)

    def __setattr__(self, name, value):
        raise AttributeError("can't set %s: frozen" % name)

    def __delattr__(self, name):
        raise AttributeError("can't delete %s: frozen" % name)


fr = Frozen(a=1, b=2)
print(fr.a, fr.b)


def thaw():
    fr.a = 2


attempt(thaw)


def remove():
    del fr.a


attempt(remove)


class Proxy:
    def __init__(self, target):
        object.__setattr__(self, "_target", target)

    def __getattr__(self, name):
        return getattr(self._target, name)

    def __setattr__(self, name, value):
        setattr(self._target, name, value)


class Target:
    def __init__(self):
        self.v = 1

    def double(self):
        return self.v * 2


target = Target()
proxy = Proxy(target)
proxy.v = 21
print(proxy.v, proxy.double(), target.v)


# ---- __dir__ ----
class Listed:
    def __init__(self):
        self.b = 1

    def __dir__(self):
        return ["zeta", "alpha", "b"]


print(dir(Listed()))


# ---- __init_subclass__ ----
class Plugin:
    registry = []

    def __init_subclass__(cls, tag=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.tag = tag or cls.__name__.lower()
        Plugin.registry.append(cls.tag)


class Alpha(Plugin):
    pass


class Beta(Plugin, tag="b"):
    pass


class Gamma(Beta):
    pass


print(Plugin.registry, Alpha.tag, Beta.tag, Gamma.tag, hasattr(Plugin, "tag"))


try:
    class Nope(tag=1):
        pass
except TypeError as e:
    print("TypeError:", e)


# ---- __class_getitem__ ----
class Box:
    def __class_getitem__(cls, item):
        return "%s[%s]" % (cls.__name__, getattr(item, "__name__", item))


print(Box[int], Box["x"], Box[Box])


class NoItems:
    pass


attempt(lambda: NoItems[int])


# ---- __new__ ----
class Single:
    instance = None

    def __new__(cls, *args):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.made = 0
        return cls.instance

    def __init__(self, value=None):
        self.made += 1
        self.value = value


a = Single(1)
b = Single(2)
print(a is b, a.value, a.made)


class Shout:
    def __new__(cls, text):
        return text.upper()

    def __init__(self, text):
        print("never runs")


print(Shout("quiet"), type(Shout("x")).__name__)


class Tracked:
    count = 0

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        Tracked.count += 1
        obj.serial = Tracked.count
        return obj

    def __init__(self, label):
        self.label = label


class TrackedChild(Tracked):
    def __init__(self, label, extra):
        super().__init__(label)
        self.extra = extra


x1 = Tracked("one")
x2 = TrackedChild("two", "more")
print(x1.serial, x1.label, x2.serial, x2.label, x2.extra, Tracked.count, type(x2).__name__)
raw = object.__new__(Tracked)
print(type(raw).__name__, hasattr(raw, "label"))


# ---- NotImplemented and the reflected methods ----
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        if isinstance(other, Money):
            return Money(self.amount + other.amount)
        if isinstance(other, int):
            return Money(self.amount + other)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, int):
            return Money(self.amount + other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Money):
            return self.amount == other.amount
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Money):
            return self.amount < other.amount
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Money):
            return self.amount <= other.amount
        return NotImplemented

    def __repr__(self):
        return "Money(%d)" % self.amount


class Coupon:
    def __radd__(self, other):
        return "coupon applied to %r" % (other,)

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return False

    def __eq__(self, other):
        return True


m = Money(5)
print(m + Money(1), m + 2, 3 + m, sum([Money(1), Money(2)]), m + Coupon())
print(m == Money(5), m == 5, m != Money(5), m != "x", m == Coupon(), Money(1) < Money(2), Money(2) <= Money(2))
print(m < Coupon(), m <= Coupon(), Money(3) > Money(2), Money(3) >= Money(4))
attempt(lambda: m + "text")
attempt(lambda: "text" + m)
attempt(lambda: m + 1.5)
attempt(lambda: m < 5)
attempt(lambda: 5 < m)
attempt(lambda: m <= "x")
attempt(lambda: m >= 3)
attempt(lambda: m - 1)
print(NotImplemented, repr(NotImplemented), type(NotImplemented).__name__, NotImplemented is NotImplemented, m.__eq__(3))
print(sorted([Money(3), Money(1), Money(2)]), max(Money(3), Money(7)), Money(1) in [Money(1)], [Money(1)].index(Money(1)))
