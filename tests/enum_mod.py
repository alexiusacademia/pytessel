# The enum module.
from enum import Enum, IntEnum, Flag, auto, unique
import enum


def attempt(f, *args):
    try:
        print(f(*args))
    except Exception as e:
        print(type(e).__name__ + ":", e)


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    def describe(self):
        return "%s is number %d" % (self.name.lower(), self.value)

    @property
    def is_primary(self):
        return True

    @classmethod
    def default(cls):
        return cls.GREEN

    @staticmethod
    def count():
        return 3


print(Color.RED, repr(Color.RED), str(Color.GREEN), Color.BLUE.name, Color.BLUE.value)
print(list(Color), len(Color), [c.name for c in Color], [c.value for c in reversed(Color)])
print(Color(1), Color(3), Color["GREEN"], Color.RED is Color(1), Color.RED is Color["RED"])
print(Color.RED == Color.RED, Color.RED == Color.GREEN, Color.RED != Color.GREEN, Color.RED == 1, Color.RED is Color.RED)
print(Color.RED.describe(), Color.BLUE.is_primary, Color.default(), Color.count(), Color.RED in Color)
print(isinstance(Color.RED, Color), isinstance(Color.RED, Enum), type(Color.RED) is Color, type(Color).__name__)
print({Color.RED: "r", Color.BLUE: "b"}[Color.BLUE], len({Color.RED, Color.RED, Color.GREEN}), sorted(c.name for c in {Color.BLUE, Color.RED}))
print(list(Color.__members__), Color.__members__["RED"] is Color.RED, Color.RED.name, f"{Color.RED.name}={Color.RED.value}")
attempt(lambda: Color(7))
attempt(lambda: Color["PURPLE"])
attempt(lambda: Color.RED < Color.GREEN)


def reassign():
    Color.RED = 10


attempt(reassign)
print(Color.RED)


def subclass_members():
    class More(Color):
        PINK = 4


attempt(subclass_members)


def light(color):
    match color:
        case Color.RED:
            return "stop"
        case Color.GREEN:
            return "go"
        case _:
            return "wait"


print([light(c) for c in Color])


class Weekday(Enum):
    MON = auto()
    TUE = auto()
    WED = auto()
    MIDWEEK = 3

    @classmethod
    def weekend(cls):
        return []


print(list(Weekday), Weekday.WED.value, Weekday.MIDWEEK is Weekday.WED, Weekday.MIDWEEK.name, list(Weekday.__members__))
print(Weekday(2), len(Weekday), Weekday.MON in Weekday)


class Planet(Enum):
    MERCURY = (3.303e23, 2.4397e6)
    EARTH = (5.976e24, 6.37814e6)

    @property
    def mass(self):
        return self.value[0]

    @property
    def radius(self):
        return self.value[1]


print(Planet.EARTH.mass, Planet.MERCURY.radius, Planet((5.976e24, 6.37814e6)).name)


class Text(Enum):
    A = "a"
    B = "b"


print(Text("a"), Text.B.value.upper(), [t.value for t in Text])


class Base(Enum):
    def shout(self):
        return self.name + "!"


class Signal(Base):
    ON = 1
    OFF = 0


print(Signal.ON.shout(), list(Signal), Signal(0))


# ---- IntEnum ----
class Level(IntEnum):
    LOW = 1
    MID = 5
    HIGH = 10


print(Level.LOW < Level.HIGH, Level.MID == 5, Level.HIGH > 7, Level.LOW + 1, Level.MID * 2, 10 - Level.LOW, int(Level.HIGH))
print(sorted([Level.HIGH, Level.LOW, Level.MID]), max(Level), repr(Level.MID), str(Level.MID), "%d" % Level.MID, f"{Level.HIGH}")
print(Level(5), Level.MID is Level(5), [1, 5, 10].index(Level.HIGH), {5: "five"}[Level.MID], list(range(Level.LOW, Level.MID)))
print(Level.LOW != 1, Level.LOW <= 1, Level.HIGH >= Level.MID, sum(Level), bool(Level.LOW), Level.MID // 2, Level.MID % 2)


# ---- Flag ----
class Perm(Flag):
    R = 4
    W = 2
    X = 1


rw = Perm.R | Perm.W
print(rw, repr(rw), rw.value, Perm.R in rw, Perm.X in rw, rw & Perm.R, bool(rw & Perm.X), rw == Perm.R | Perm.W)
print(list(rw), Perm(7), Perm(0), ~Perm.R, rw ^ Perm.R, Perm.R | Perm.R)


class Bits(Flag):
    A = auto()
    B = auto()
    C = auto()


print([b.value for b in Bits], Bits.A | Bits.C, (Bits.A | Bits.C).value)


# ---- unique ----
@unique
class Fine(Enum):
    ONE = 1
    TWO = 2


print(list(Fine))


def duplicated():
    @unique
    class Twice(Enum):
        ONE = 1
        UNO = 1

    return Twice


attempt(duplicated)
print(enum.Enum is Enum, enum.auto is auto)
