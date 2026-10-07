# Classes, inheritance, special methods, properties.
class Point:
    count = 0

    def __init__(self, x, y=0):
        self.x = x
        self.y = y
        Point.count += 1

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __len__(self):
        return 2

    def __getitem__(self, i):
        return (self.x, self.y)[i]

    def norm2(self):
        return self.x ** 2 + self.y ** 2

p = Point(1, 2)
q = Point(3)
print(p, q, p + q, p == Point(1, 2), p != q, p < q, len(p), p[0], p[1], Point.count)
print(sorted([Point(2, 1), Point(1, 5), Point(1, 2)]), p.norm2(), list(p), isinstance(p, Point))
p.z = 9
print(p.z, hasattr(p, "z"), hasattr(p, "w"), getattr(p, "w", "none"), type(p).__name__)

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

    def __str__(self):
        return f"<{type(self).__name__} {self.name}>"

class Dog(Animal):
    def __init__(self, name, tricks=None):
        super().__init__(name)
        self.tricks = tricks or []

    def speak(self):
        return super().speak() + ": woof"

class Puppy(Dog):
    pass

d = Puppy("Rex", ["sit"])
print(d, d.speak(), d.tricks, isinstance(d, Animal), isinstance(d, Dog), issubclass(Puppy, Animal), issubclass(Animal, Dog))

class Temperature:
    def __init__(self, celsius):
        self._c = celsius

    @property
    def fahrenheit(self):
        return self._c * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, f):
        self._c = (f - 32) * 5 / 9

    @staticmethod
    def freezing():
        return 0

    @classmethod
    def boiling(cls):
        return cls(100)

t = Temperature(25)
print(t.fahrenheit, Temperature.freezing(), Temperature.boiling().fahrenheit)
t.fahrenheit = 212
print(t._c)

class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)
        return self

    def __bool__(self):
        return bool(self.items)

    def __contains__(self, x):
        return x in self.items

    def __iter__(self):
        return iter(self.items)

    def __call__(self, n):
        return self.items[n]

s = Stack()
print(bool(s), s.push(1).push(2).items, bool(s), 2 in s, 5 in s, [x * 2 for x in s], s(0))

class A:
    def who(self):
        return "A"
class B(A):
    def who(self):
        return "B" + super().who()
class C(A):
    def who(self):
        return "C" + super().who()
class D(B, C):
    def who(self):
        return "D" + super().who()
print(D().who())

class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1
print(list(Countdown(3)), [x for x in Countdown(2)])

class Managed:
    def __enter__(self):
        print("enter")
        return "resource"
    def __exit__(self, kind, value, tb):
        print("exit", kind is None)
        return False
with Managed() as r:
    print("inside", r)
print(Point.__name__, p.__class__.__name__, p.__dict__)
