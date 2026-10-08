# The match statement (PEP 634).

# ---- match and case stay ordinary names ----
match = 3
case = 4
print(match + case)
match += 1
print(match)
match, case = case, match
print(match, case)


def match_fn(match, case=2):
    return match * case


print(match_fn(5))
d = {"match": 1}
print(d["match"])
match = [1, 2, 3]
print(match[0], match[-1])
match[0] = 10
print(match)


class Finder:
    def match(self, text):
        return "matched " + text

    case = "attribute"


f = Finder()
print(f.match("x"), f.case)
match = f.match
print(match("y"))
print(match
      ("z"))


# ---- literals ----
def literal(x):
    match x:
        case 0:
            return "zero"
        case 1 | 2 | 3:
            return "small"
        case -1:
            return "minus one"
        case 2.5:
            return "two and a half"
        case "hello":
            return "greeting"
        case "a" "b":
            return "joined"
        case None:
            return "nothing"
        case True:
            return "yes"
        case False:
            return "no"
        case _:
            return "other"


for v in [0, 1, 3, -1, 2.5, "hello", "ab", None, True, False, 99, "x", [], 0.0, 1.0]:
    print(repr(v), "->", literal(v))


# (True is 1 and False is 0 for a number, but not the other way round.)
def truth(x):
    match x:
        case True:
            return "True itself"
        case 1:
            return "one"
        case _:
            return "else"


print(truth(True), truth(1), truth(1.0), truth(2))


# ---- captures and wildcard ----
def capture(x):
    match x:
        case [a, b]:
            return "pair %r %r" % (a, b)
        case other:
            return "got %r" % (other,)


print(capture([1, 2]))
print(capture("xy"))
print(capture(7))

match 42:
    case n:
        pass
print(n)

match 5:
    case _:
        print("wildcard takes nothing")
try:
    print(_)
except NameError as e:
    print("NameError:", e)


# ---- value patterns ----
class Color:
    RED = 1
    GREEN = 2
    BLUE = 3


class Config:
    class Limits:
        MAX = 100


def color(c):
    match c:
        case Color.RED:
            return "red"
        case Color.GREEN | Color.BLUE:
            return "cool"
        case Config.Limits.MAX:
            return "max"
        case _:
            return "unknown"


print([color(c) for c in (1, 2, 3, 100, 4)])


# ---- sequences ----
def seq(x):
    match x:
        case []:
            return "empty"
        case [a]:
            return "one: %r" % (a,)
        case [a, b]:
            return "two: %r %r" % (a, b)
        case [first, *rest]:
            return "first %r rest %r" % (first, rest)


for v in [[], [1], (1,), [1, 2], (1, 2), [1, 2, 3], (1, 2, 3, 4), range(2), range(5)]:
    print(seq(v))
print(seq("ab"), seq({1, 2}), seq({"a": 1}), seq(5))


def star(x):
    match x:
        case [*_, 0]:
            return "ends with zero"
        case [1, *middle, 9]:
            return "1..9 around %r" % (middle,)
        case (a, b, *_):
            return "starts %r %r" % (a, b)
        case [*all]:
            return "all %r" % (all,)


print(star([5, 0]), star([0]), star([1, 9]), star([1, 2, 3, 9]), star([4, 5, 6]), star([7]), star([]))

match (1, 2, 3):
    case a, b, c:
        print("open sequence", a, b, c)

match [1, [2, [3, 4]]]:
    case [x, [y, [z, w]]]:
        print("nested", x, y, z, w)

match "text":
    case [*chars]:
        print("a string is not a sequence here")
    case str() as s:
        print("string", s)

match (1,):
    case (x,):
        print("one-tuple", x)

match 5:
    case (x):
        print("group", x)

match [1, 2]:
    case [1, 2, *rest]:
        print("empty rest", rest)


# ---- mappings ----
def mapping(x):
    match x:
        case {"type": "circle", "r": r}:
            return "circle %r" % (r,)
        case {"type": "rect", "w": w, "h": h}:
            return "rect %rx%r" % (w, h)
        case {"type": t, **rest}:
            return "other %r with %r" % (t, rest)
        case {}:
            return "some dict"
        case _:
            return "not a dict"


print(mapping({"type": "circle", "r": 2}))
print(mapping({"type": "circle", "r": 2, "extra": True}))
print(mapping({"type": "rect", "w": 3, "h": 4}))
print(mapping({"type": "line", "a": 1, "b": 2}))
print(mapping({"x": 1}))
print(mapping({}))
print(mapping([("type", "circle")]))

match {1: "one", 2: "two", None: "none", True: "t"}:
    case {1: a, 2: b, None: c}:
        print(a, b, c)

match {"a": {"b": [1, 2]}}:
    case {"a": {"b": [x, y]}}:
        print("deep", x, y)

match {"k": 1}:
    case {"missing": v}:
        print("no")
    case {"k": 2}:
        print("no")
    case {"k": 1 | 2 as v}:
        print("k is", v)


# ---- classes ----
class Point:
    __match_args__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Point3(Point):
    __match_args__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        Point.__init__(self, x, y)
        self.z = z


class Plain:
    def __init__(self, **kw):
        for k in kw:
            setattr(self, k, kw[k])


def where(p):
    match p:
        case Point(x=0, y=0):
            return "origin"
        case Point(x=0, y=y):
            return "on y axis at %r" % (y,)
        case Point(x, 0):
            return "on x axis at %r" % (x,)
        case Point3(x, y, z):
            return "3d %r %r %r" % (x, y, z)
        case Point(x, y) if x == y:
            return "diagonal %r" % (x,)
        case Point():
            return "somewhere"
        case Plain(name=n, size=s):
            return "plain %r %r" % (n, s)
        case Plain():
            return "plain without"
        case _:
            return "not a point"


print(where(Point(0, 0)))
print(where(Point(0, 5)))
print(where(Point(5, 0)))
print(where(Point3(1, 2, 3)))
print(where(Point3(0, 2, 3)))
print(where(Point(4, 4)))
print(where(Point(4, 5)))
print(where(Plain(name="n", size=2)))
print(where(Plain(name="n")))
print(where((0, 0)))


def builtin(x):
    match x:
        case bool(b):
            return "bool %r" % (b,)
        case int(n):
            return "int %r" % (n,)
        case float(f):
            return "float %r" % (f,)
        case str(s):
            return "str %r" % (s,)
        case list(items):
            return "list %r" % (items,)
        case tuple(items):
            return "tuple %r" % (items,)
        case dict(d):
            return "dict %r" % (d,)
        case set():
            return "a set"
        case None:
            return "None"
        case object():
            return "an object"


for v in [True, 3, 2.5, "s", [1], (1,), {"a": 1}, {1}, None, Point(1, 2)]:
    print(builtin(v))

match 3:
    case int() | float() as number:
        print("number", number)

match 2.0:
    case int():
        print("no")
    case float():
        print("float() without a pattern")

match [Point(1, 2), Point(3, 4)]:
    case [Point(x=a), Point(y=b)]:
        print("points", a, b)

match {"p": Point(1, 2)}:
    case {"p": Point(x, y)}:
        print("in a dict", x, y)

match ValueError("bad", 2):
    case KeyError():
        print("no")
    case ValueError(args=(msg, code)):
        print("exception", msg, code)


# ---- OR and AS ----
def either(x):
    match x:
        case ("go", ("north" | "south") as d) | ("move", d):
            return "direction " + d
        case [("a" | "b") as letter, n] | [n, ("a" | "b") as letter]:
            return "letter %s number %r" % (letter, n)
        case (1 | 2) as small:
            return "small %r" % (small,)
        case [x, y] as whole:
            return "whole %r" % (whole,)
        case _:
            return "none"


print(either(("go", "north")))
print(either(("move", "up")))
print(either(("a", 1)))
print(either((2, "b")))
print(either(2))
print(either([8, 9]))
print(either("nothing"))


# ---- guards ----
def sign(x):
    match x:
        case int(n) if n > 0:
            return "positive"
        case int(n) if n < 0:
            return "negative"
        case 0:
            return "zero"
        case n if isinstance(n, float):
            return "a float"
    return "no case"


print(sign(5), sign(-5), sign(0), sign(1.5), sign("s"))

# A name keeps the value a pattern gave it, even when the guard said no.
match 10:
    case kept if kept > 100:
        print("no")
    case _:
        print("kept is", kept)

# A pattern that fails gives no name a value.
before = "untouched"
match [1, "x"]:
    case [before, 2]:
        print("no")
    case _:
        print("before is", before)

# No case fits: nothing runs.
match 99:
    case 1:
        print("no")
    case 2:
        print("no")
print("after no match")


# ---- the subject is worked out once; cases in order ----
calls = []


def subject():
    calls.append("subject")
    return 3


match subject():
    case 1:
        pass
    case 3:
        calls.append("three")
    case _:
        calls.append("default")
print(calls)

# ---- match in loops, with break / continue / return ----
out = []
for item in [1, "skip", 2, "stop", 3]:
    match item:
        case "skip":
            continue
        case "stop":
            break
        case int(n):
            out.append(n * 10)
print(out)


def commands(lines):
    total = 0
    for line in lines:
        match line.split():
            case ["add", n]:
                total += int(n)
            case ["sub", n]:
                total -= int(n)
            case ["quit"]:
                return total
            case ["add" | "sub"]:
                print("missing number")
            case [word, *args]:
                print("unknown", word, len(args))
            case []:
                print("blank")
    return total


print(commands(["add 5", "sub 2", "add", "mul 2 3", "", "add 10", "quit", "add 100"]))


# ---- nested match, match in a class, match as an expression's part ----
def nested(a, b):
    match a:
        case 1:
            match b:
                case 1:
                    return "1-1"
                case _:
                    return "1-other"
        case _:
            match b:
                case 1:
                    return "other-1"
    return "none"


print(nested(1, 1), nested(1, 2), nested(2, 1), nested(2, 2))


class Shape:
    def __init__(self, kind, *sizes):
        self.kind = kind
        self.sizes = sizes

    def area(self):
        match self.kind, self.sizes:
            case "square", (s,):
                return s * s
            case "rect", (w, h):
                return w * h
            case kind, _:
                raise ValueError("no area for " + kind)


print(Shape("square", 3).area(), Shape("rect", 2, 5).area())
try:
    Shape("blob").area()
except ValueError as e:
    print("ValueError:", e)


# ---- in a generator ----
def tokens(items):
    for item in items:
        match item:
            case int() | float():
                yield "number"
            case str() if item.isalpha():
                yield "word"
            case [*parts]:
                yield "group of %d" % len(parts)
                for p in parts:
                    yield "  part %r" % (p,)
            case _:
                yield "other"


print(list(tokens([1, "abc", "a1", [1, 2], 2.5, None])))

# ---- a subject with commas, a starred subject, a walrus guard ----
x, y = 1, 2
match x, y:
    case 1, 2:
        print("tuple subject")

match *[1, 2], 3:
    case [1, 2, 3]:
        print("starred subject")

match 12:
    case n if (half := n // 2) > 5:
        print("half", half)


# ---- errors at run time ----
class NoArgs:
    pass


class BadArgs:
    __match_args__ = ["a"]


class TwoArgs:
    __match_args__ = ("a", "a")

    def __init__(self):
        self.a = 1


def run_case(value, pattern):
    try:
        match_source = "match value:\n    case " + pattern + ":\n        print('matched')\n    case _:\n        print('no match')\n"
        exec(match_source)
    except Exception as e:
        print(type(e).__name__ + ":", e)


run_case(NoArgs(), "NoArgs(x)")
run_case(BadArgs(), "BadArgs(x)")
run_case(TwoArgs(), "TwoArgs(x, y)")
run_case(Point(1, 2), "Point(x, y, z)")
run_case(Point(1, 2), "Point(x, x=1)")
run_case(3, "int(a, b)")
run_case(3, "value()")
run_case({"a": 1}, "{'a': 1, 'a': 2}")
run_case(Point(1, 2), "Point(q=1)")
run_case(3, "int(real=3)")
run_case("s", "str(upper=u)")


# ---- syntax errors ----
def bad(source):
    try:
        exec(source)
    except SyntaxError as e:
        print("SyntaxError:", e.msg)
    else:
        print("no error")


bad("match x:\n    case _:\n        pass\n    case 1:\n        pass\n")
bad("match x:\n    case y:\n        pass\n    case 1:\n        pass\n")
bad("match x:\n    case y if y:\n        pass\n    case 1:\n        pass\n")
bad("match x:\n    case [a, a]:\n        pass\n")
bad("match x:\n    case [*a, *b]:\n        pass\n")
bad("match x:\n    case [a] | [b]:\n        pass\n")
bad("match x:\n    case a | 1:\n        pass\n")
bad("match x:\n    case _ | 1:\n        pass\n")
bad("match x:\n    case 1 | a:\n        pass\n    case 2:\n        pass\n")
bad("match x:\n    case Point(x=1, x=2):\n        pass\n")
bad("match x:\n    case Point(x=1, 2):\n        pass\n")
bad("match x:\n    case 1 as _:\n        pass\n")
bad("match x:\n    case {'a': a, **a}:\n        pass\n")
bad("match x:\n    case (a as b) as a:\n        pass\n")
bad("x = 1\nmatch x:\n    case [1, _] | _ as y:\n        pass\nprint('fine', y)\n")
