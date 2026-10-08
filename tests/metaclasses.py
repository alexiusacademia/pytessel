# Metaclasses, type() with three arguments, abstract classes.
from abc import ABC, ABCMeta, abstractmethod


def attempt(f, *args):
    try:
        print(f(*args))
    except Exception as e:
        print(type(e).__name__ + ":", e)


# ---- type(name, bases, namespace) ----
def describe(self):
    return "%s with %d" % (type(self).__name__, self.size)


Made = type("Made", (), {"size": 3, "describe": describe})
m = Made()
print(Made.__name__, m.size, m.describe(), type(m) is Made, isinstance(m, Made), type(Made) is type)
Child = type("Child", (Made,), {"size": 5, "extra": lambda self: "extra"})
c = Child()
print(c.describe(), c.extra(), isinstance(c, Made), issubclass(Child, Made), Child.__bases__ == (Made,), Child.__mro__[1] is Made)
print(type(3), type("s"), type(None).__name__, type(type), type(Made).__name__, type(int) is type)
attempt(lambda: type("Bad", (), {}, 1))
attempt(lambda: type("Bad", [], {}))
attempt(lambda: type(1, (), {}))
print(isinstance(Made, type), isinstance(m, type), isinstance(int, type), isinstance(3, type), issubclass(type, object))


# ---- a metaclass: __new__ and __init__ ----
class Meta(type):
    created = []

    def __new__(mcs, name, bases, namespace):
        namespace["added_by_meta"] = name.lower()
        cls = super().__new__(mcs, name, bases, namespace)
        Meta.created.append(name)
        return cls

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls.base_count = len(bases)


class Base(metaclass=Meta):
    def hello(self):
        return "hello from " + self.added_by_meta


class Derived(Base):
    pass


class Other:
    pass


class Mixed(Other, Derived):
    pass


print(Meta.created, Base.added_by_meta, Derived.added_by_meta, Base.base_count, Derived.base_count, Mixed.base_count)
print(Base().hello(), Derived().hello(), type(Base) is Meta, type(Derived) is Meta, type(Mixed) is Meta, type(Other) is type)
print(isinstance(Base, Meta), isinstance(Derived, Meta), isinstance(Other, Meta), isinstance(Base(), Base), isinstance(Base, type))
print(type(Base).__name__, Base.__class__ is Meta, issubclass(Meta, type), isinstance(Meta, type))


# ---- methods and properties of the metaclass are the class's own ----
class Registry(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "plugins"):
            cls.plugins = {}
        else:
            cls.plugins[name.lower()] = cls

    def create(cls, kind, *args):
        return cls.plugins[kind](*args)

    @property
    def kinds(cls):
        return sorted(cls.plugins)

    def __repr__(cls):
        return "<plugin class %s>" % cls.__name__

    def __len__(cls):
        return len(cls.plugins)

    def __iter__(cls):
        return iter(sorted(cls.plugins.values(), key=lambda p: p.__name__))

    def __contains__(cls, kind):
        return kind in cls.plugins

    def __getitem__(cls, kind):
        return cls.plugins[kind]


class Shape(metaclass=Registry):
    def __init__(self, size=1):
        self.size = size

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.size)


class Square(Shape):
    pass


class Circle(Shape):
    pass


print(Shape.kinds, Shape.create("square", 4), Shape.create("circle"), Shape, Square, [Circle], str(Square))
print(len(Shape), list(Shape), "square" in Shape, "hexagon" in Shape, Shape["circle"], [s.__name__ for s in Shape])
attempt(lambda: Square().create)
attempt(lambda: Square().kinds)
attempt(lambda: Shape["hexagon"])


# ---- a metaclass's __call__: what Class(…) does ----
class SingletonMeta(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in SingletonMeta.instances:
            SingletonMeta.instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMeta.instances[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self, name="default"):
        print("Config made:", name)
        self.name = name


class Cache(metaclass=SingletonMeta):
    pass


a = Config("first")
b = Config("second")
print(a is b, a.name, Cache() is Cache(), Cache() is a, len(SingletonMeta.instances))


class Counting(type):
    def __call__(cls, *args):
        obj = type.__call__(cls, *args)
        obj.args = args
        cls.count = getattr(cls, "count", 0) + 1
        return obj


class Counted(metaclass=Counting):
    def __init__(self, *args):
        self.total = sum(args)


x = Counted(1, 2, 3)
y = Counted()
print(x.total, x.args, y.total, y.args, Counted.count)


# ---- keywords of the class statement reach the metaclass ----
class Options(type):
    def __new__(mcs, name, bases, namespace, **options):
        cls = super().__new__(mcs, name, bases, namespace)
        cls.options = options
        return cls

    def __init__(cls, name, bases, namespace, **options):
        super().__init__(name, bases, namespace)


class Table(metaclass=Options, table="users", strict=True):
    pass


class Plain(metaclass=Options):
    pass


print(sorted(Table.options.items()), Plain.options)


# ---- a metaclass can check or change what the class body made ----
class NoCamel(type):
    def __new__(mcs, name, bases, namespace):
        for key in namespace:
            if key != key.lower():
                raise NameError("%s.%s: use lower_case names" % (name, key))
        return super().__new__(mcs, name, bases, namespace)


try:
    class Bad(metaclass=NoCamel):
        def doThing(self):
            pass
except NameError as e:
    print("NameError:", e)


class Upper(type):
    def __new__(mcs, name, bases, namespace):
        shouted = {}
        for key, value in namespace.items():
            shouted[key if key.startswith("__") else key.upper()] = value
        return type.__new__(mcs, name, bases, shouted)


class Loud(metaclass=Upper):
    volume = 11

    def speak(self):
        return "LOUD"


print(Loud.VOLUME, Loud().SPEAK(), hasattr(Loud, "volume"), hasattr(Loud, "speak"))


# ---- an enum, the way the library makes one ----
class EnumMeta(type):
    def __new__(mcs, name, bases, namespace):
        members = {}
        for key, value in list(namespace.items()):
            if not key.startswith("_") and not callable(value):
                members[key] = value
        cls = super().__new__(mcs, name, bases, namespace)
        cls._members = {}
        for key, value in members.items():
            member = object.__new__(cls)
            member.name = key
            member.value = value
            setattr(cls, key, member)
            cls._members[key] = member
        return cls

    def __iter__(cls):
        return iter(cls._members.values())

    def __len__(cls):
        return len(cls._members)

    def __getitem__(cls, name):
        return cls._members[name]

    def __call__(cls, value):
        for member in cls._members.values():
            if member.value == value:
                return member
        raise ValueError("%r is not a valid %s" % (value, cls.__name__))

    def __contains__(cls, member):
        return isinstance(member, cls) and member.name in cls._members


class Enum(metaclass=EnumMeta):
    def __repr__(self):
        return "<%s.%s: %r>" % (type(self).__name__, self.name, self.value)

    def __str__(self):
        return "%s.%s" % (type(self).__name__, self.name)


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    def is_warm(self):
        return self is Color.RED


class Weekday(Enum):
    MON = "mon"
    TUE = "tue"


print(Color.RED, repr(Color.GREEN), Color.BLUE.name, Color.BLUE.value, list(Color), len(Color))
print(Color(2), Color["BLUE"], Color.RED is Color(1), Color.RED == Color.RED, Color.RED != Color.GREEN, Color.RED.is_warm(),
      Color.BLUE.is_warm())
print(Color.RED in Color, Weekday.MON in Color, isinstance(Color.RED, Color), isinstance(Color.RED, Enum), type(Color.RED) is Color)
print([str(d) for d in Weekday], Weekday("tue"), {Color.RED: "r", Color.GREEN: "g"}[Color.GREEN])
attempt(lambda: Color(9))
attempt(lambda: Color["PINK"])


def pick(color):
    match color:
        case Color.RED:
            return "stop"
        case Color.GREEN:
            return "go"
        case _:
            return "?"


print(pick(Color.RED), pick(Color.GREEN), pick(Color.BLUE))


# ---- abc ----
class Animal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def sound(self):
        ...

    @abstractmethod
    def legs(self):
        return 4

    def describe(self):
        return "%s says %s on %d legs" % (self.name, self.sound(), self.legs())


class Dog(Animal):
    def sound(self):
        return "woof"

    def legs(self):
        return super().legs()


class Half(Animal):
    def sound(self):
        return "..."


class Bird(Half):
    def legs(self):
        return 2


print(Dog("Rex").describe(), Bird("Tweety").describe())
attempt(lambda: Animal("x"))
attempt(lambda: Half("x"))
print(isinstance(Dog("d"), Animal), issubclass(Bird, Animal), type(Animal) is ABCMeta, type(Dog).__name__,
      sorted(Animal.__abstractmethods__), sorted(Half.__abstractmethods__), sorted(Dog.__abstractmethods__))


class Sized(metaclass=ABCMeta):
    @property
    @abstractmethod
    def size(self):
        ...

    @classmethod
    @abstractmethod
    def make(cls):
        ...

    @staticmethod
    @abstractmethod
    def unit():
        ...


class Three(Sized):
    @property
    def size(self):
        return 3

    @classmethod
    def make(cls):
        return cls()

    @staticmethod
    def unit():
        return "cm"


attempt(lambda: Sized())
print(Three.make().size, Three.unit())


class OnlyOne(ABC):
    @abstractmethod
    def run(self):
        pass


attempt(OnlyOne)


class NotAbstract(ABC):
    def run(self):
        return "ran"


print(NotAbstract().run())
