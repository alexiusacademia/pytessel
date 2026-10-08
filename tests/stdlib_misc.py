# The smaller modules: operator, copy, textwrap, bisect, heapq; and what
# time has for dates.
#
# Author: Alexius Academia
# Date: 2026-10-08
import operator
import copy
import textwrap
import bisect
import heapq
import time
from operator import itemgetter, attrgetter, methodcaller
from functools import reduce

# ---- operator: the operators as functions ----
print(operator.add(2, 3), operator.sub(2, 3), operator.mul(4, 5), operator.truediv(7, 2), operator.floordiv(7, 2))
print(operator.mod(7, 3), operator.pow(2, 10), operator.neg(5), operator.pos(-5), operator.abs(-7), operator.abs(-2.5))
print(operator.lt(1, 2), operator.le(2, 2), operator.eq(1, 1.0), operator.ne(1, 2), operator.ge(1, 2), operator.gt(3, 2))
print(operator.and_(6, 3), operator.or_(6, 3), operator.xor(6, 3), operator.inv(5), operator.invert(0), operator.lshift(1, 4), operator.rshift(64, 2))
print(operator.not_(0), operator.not_([1]), operator.truth([]), operator.truth("x"), operator.is_(None, None), operator.is_not(1, None))
print(operator.concat([1], [2]), operator.concat("a", "b"), operator.contains([1, 2], 2), operator.contains("abc", "z"))
print(operator.countOf([1, 2, 1, 1], 1), operator.indexOf("hello", "l"), operator.getitem([5, 6, 7], 1), operator.getitem({"k": "v"}, "k"))
items = [1, 2, 3]
operator.setitem(items, 0, 9)
operator.delitem(items, 1)
print(items, operator.index(5), operator.length_hint([1, 2]), operator.length_hint(5, 7))
print(reduce(operator.mul, range(1, 7)), reduce(operator.add, ["a", "b", "c"]), list(map(operator.neg, [1, -2])))
print(sorted([3, 1, 2], key=operator.neg), list(map(operator.add, [1, 2], [10, 20])))
print(operator.iadd([1], [2]), operator.isub(5, 2), operator.imul(3, 4), operator.itruediv(1, 4), operator.ifloordiv(9, 2), operator.imod(9, 4))
target = [1]
print(operator.iadd(target, [2]) is target, target, operator.iconcat(target, [3]), operator.ipow(2, 5), operator.iand(7, 2), operator.ior(4, 1), operator.ixor(5, 1), operator.ilshift(1, 3), operator.irshift(8, 1))
print(operator.__add__(1, 2), operator.__lt__(1, 2), operator.__getitem__("abc", 1), operator.__contains__("abc", "b"))
try:
    operator.indexOf([1, 2], 3)
except ValueError as e:
    print("ValueError", e)
try:
    operator.index(1.5)
except TypeError as e:
    print("TypeError", e)
try:
    operator.add(1, "a")
except TypeError as e:
    print("TypeError", e)

# ---- itemgetter, attrgetter, methodcaller ----
rows = [("pear", 3, 0.5), ("apple", 7, 0.25), ("fig", 3, 2.0)]
print(sorted(rows, key=itemgetter(1)), sorted(rows, key=itemgetter(1, 0)), sorted(rows, key=itemgetter(2), reverse=True))
print(itemgetter(0)(rows[0]), itemgetter(0, 2)(rows[0]), itemgetter(-1)("abc"), itemgetter("k")({"k": 1}), itemgetter(1, 1, 0)("xy"))
print(list(map(itemgetter(0), rows)), max(rows, key=itemgetter(2))[0], min(rows, key=itemgetter(1, 2))[0])
print(dict(sorted({"b": 2, "a": 3, "c": 1}.items(), key=itemgetter(1))))
try:
    itemgetter(5)([1])
except IndexError as e:
    print("IndexError", e)
try:
    itemgetter("x")({})
except KeyError as e:
    print("KeyError", e)


class Owner:
    def __init__(self, name):
        self.name = name


class Pet:
    def __init__(self, name, age, owner):
        self.name = name
        self.age = age
        self.owner = Owner(owner)

    def speak(self, sound="hi", times=1):
        return self.name + ": " + " ".join([sound] * times)


pets = [Pet("Rex", 5, "ann"), Pet("Tom", 2, "cy"), Pet("Ada", 9, "bob")]
print([p.name for p in sorted(pets, key=attrgetter("age"))], [p.name for p in sorted(pets, key=attrgetter("owner.name"))])
print(attrgetter("name")(pets[0]), attrgetter("name", "age")(pets[1]), attrgetter("owner.name", "age")(pets[2]))
print(list(map(attrgetter("age"), pets)), max(pets, key=attrgetter("age")).name)
try:
    attrgetter("nope")(pets[0])
except AttributeError as e:
    print("AttributeError", e)
try:
    attrgetter(1)
except TypeError as e:
    print("TypeError", e)
print(methodcaller("upper")("abc"), methodcaller("split", ",")("a,b"), methodcaller("replace", "a", "b")("banana"))
print(methodcaller("speak")(pets[0]), methodcaller("speak", "woof", times=2)(pets[0]), methodcaller("speak", sound="yo")(pets[1]))
print(list(map(methodcaller("strip"), [" a ", "b  "])), sorted(["b", "A", "c"], key=methodcaller("lower")))
print(methodcaller("get", "k", 0)({"k": 5}), methodcaller("count", 1)([1, 1, 2]))
try:
    methodcaller("nope")("abc")
except AttributeError as e:
    print("AttributeError", e)

# ---- copy ----
a = [1, [2, 3], {"k": [4]}]
shallow = copy.copy(a)
deep = copy.deepcopy(a)
a[1].append(99)
a[2]["k"].append(5)
a.append("end")
print(shallow, deep, shallow is a, shallow[1] is a[1], deep[1] is a[1])
d = {"a": [1], "b": {"c": (1, [2])}}
d2 = copy.copy(d)
d3 = copy.deepcopy(d)
d["a"].append(2)
d["b"]["c"][1].append(3)
d["new"] = 1
print(d2, d3, sorted(d3))
s = {1, 2}
s2 = copy.copy(s)
s.add(3)
print(sorted(s2), copy.deepcopy({(1, 2), 3}) == {(1, 2), 3})
t = (1, [2], "x")
t2 = copy.deepcopy(t)
t[1].append(3)
print(t2, copy.copy(t) is t, copy.deepcopy((1, 2, "a")) == (1, 2, "a"))
for value in [1, 2.5, "text", None, True, len, int, range(3)]:
    print(copy.copy(value) is value or copy.copy(value) == value, copy.deepcopy(value) is value or copy.deepcopy(value) == value, end=" ")
print()


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def __repr__(self):
        return "Node(%r, %r)" % (self.value, self.children)


tree = Node(1, [Node(2), Node(3, [Node(4)])])
flat = copy.copy(tree)
full = copy.deepcopy(tree)
tree.children[0].value = "changed"
tree.children.append(Node(5))
tree.value = 100
print(flat, full, tree)
print(flat.children is tree.children, full.children is tree.children, type(full) is Node, isinstance(flat, Node))
shared = [1]
both = [shared, shared]
copied = copy.deepcopy(both)
copied[0].append(2)
print(copied, copied[0] is copied[1], both)
loop = [1]
loop.append(loop)
looped = copy.deepcopy(loop)
print(looped[0], looped[1] is looped, looped is loop)
n = Node("self")
n.children.append(n)
m = copy.deepcopy(n)
print(m.children[0] is m, m is n, m.value)


class Custom:
    def __init__(self, tag):
        self.tag = tag

    def __copy__(self):
        return Custom(self.tag + " (copy)")

    def __deepcopy__(self, memo):
        return Custom(self.tag + " (deep copy)")


print(copy.copy(Custom("c")).tag, copy.deepcopy(Custom("c")).tag, copy.deepcopy([Custom("in list")])[0].tag)
matrix = [[0] * 3 for _ in range(2)]
clone = copy.deepcopy(matrix)
clone[0][0] = 1
print(matrix, clone, copy.deepcopy([]), copy.deepcopy({}), copy.copy(""), copy.deepcopy([[[[1]]]]))

# ---- textwrap ----
text = ("The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs! "
        "How vexingly quick daft zebras jump; sphinx of black quartz, judge my vow.")
for line in textwrap.wrap(text, 30):
    print("|" + line + "|")
print(textwrap.fill(text, 50))
print(textwrap.fill(text, 40, initial_indent="* ", subsequent_indent="  "))
print(textwrap.wrap("short", 20), textwrap.wrap("", 20), textwrap.wrap("   ", 20), textwrap.wrap("a b", 1))
print(textwrap.wrap("Supercalifragilisticexpialidocious is long", 10))
print(textwrap.wrap("Supercalifragilisticexpialidocious is long", 10, break_long_words=False))
print(textwrap.wrap("a well-known hyphen-ated phrase-book entry", 12))
print(textwrap.wrap("a well-known hyphen-ated phrase-book entry", 12, break_on_hyphens=False))
print(textwrap.wrap("tabs\tand\nnewlines   and   spaces", 12))
print(textwrap.wrap("tabs\tand\nnewlines", 40, expand_tabs=False, replace_whitespace=False))
print(textwrap.wrap("  leading and trailing  ", 10), textwrap.wrap("  leading and trailing  ", 10, drop_whitespace=False))
print(textwrap.wrap("End. Next one? Yes! Done.", 60, fix_sentence_endings=True))
print(textwrap.wrap("one two three four five six seven", 10, max_lines=2))
print(textwrap.wrap("one two three four five six seven", 10, max_lines=2, placeholder="..."))
print(textwrap.wrap("x" * 25, 10), textwrap.wrap("a--b and c -- d", 6), textwrap.wrap("1,000,000 2.5 e.g. i.e.", 9))
print(textwrap.fill("Hello world, this is a test.", width=12).split("\n"))
print(textwrap.shorten("Hello  world, this   is a test.", 20), "|", textwrap.shorten("Hello world", 20), "|", textwrap.shorten("Hello world!", 11))
print(textwrap.shorten("Hello world, this is a test.", 15, placeholder="..."), "|", textwrap.shorten("  spaced \n out  ", 50), "|", textwrap.shorten("word", 6))
try:
    textwrap.wrap("abc", 0)
except ValueError as e:
    print("ValueError", e)
try:
    textwrap.shorten("some long text here", 3)
except ValueError as e:
    print("ValueError", e)
block = """
    def f():
        return 1

    x = f()
"""
print(repr(textwrap.dedent(block)))
print(repr(textwrap.dedent("  a\n    b\n  c")), repr(textwrap.dedent("a\n  b")), repr(textwrap.dedent("\tx\n\ty")), repr(textwrap.dedent("  a\n\tb")))
print(repr(textwrap.dedent("    one\n   \n    two\n")), repr(textwrap.dedent("")), repr(textwrap.dedent("  only")), repr(textwrap.dedent("   a\n  b\n    c")))
print(repr(textwrap.indent("a\nb\n", "  ")), repr(textwrap.indent("a\n\n  \nb", "> ")), repr(textwrap.indent("a\n\nb", "> ", lambda line: True)))
print(repr(textwrap.indent("one\ntwo\nthree", "+ ", lambda line: "t" in line)), repr(textwrap.indent("", "  ")), repr(textwrap.indent("x", "\t")))
print(textwrap.indent(textwrap.fill("wrap me then indent me, please and thank you", 16), "    "))
print(textwrap.dedent(textwrap.indent("a\n b\n", "  ")) == "a\n b\n")
w = textwrap.TextWrapper(width=15, initial_indent="- ")
print(w.wrap("first item of the list"), w.fill("second"), w.width)

# ---- bisect ----
grades = [60, 70, 80, 90]
print([bisect.bisect(grades, score) for score in [33, 60, 65, 70, 89, 90, 100]])
print([bisect.bisect_left(grades, score) for score in [33, 60, 65, 70, 89, 90, 100]])
print([bisect.bisect_right(grades, score) for score in [59, 60, 61]], bisect.bisect([], 1), bisect.bisect_left([], 1))
print(["FDCBA"[bisect.bisect(grades, score)] for score in [33, 99, 77, 70, 89, 90, 100]])
values = [1, 2, 2, 2, 3]
print(bisect.bisect_left(values, 2), bisect.bisect_right(values, 2), bisect.bisect_left(values, 2, 2), bisect.bisect_right(values, 2, 0, 2), bisect.bisect_left(values, 2, lo=1, hi=3))
ordered = []
for n in [5, 1, 4, 1, 3, 9, 2, 6]:
    bisect.insort(ordered, n)
print(ordered)
lefts = [1, 2, 3]
bisect.insort_left(lefts, 2)
bisect.insort_right(lefts, 0)
bisect.insort(lefts, 10)
print(lefts, bisect.bisect(["a", "c"], "b"), bisect.bisect_left([1.5, 2.5], 2), bisect.bisect([(1, "a"), (2, "b")], (1, "z")))
try:
    bisect.bisect([1, 2], 1, -1)
except ValueError as e:
    print("ValueError", e)


def find(sorted_values, x):
    i = bisect.bisect_left(sorted_values, x)
    return i if i < len(sorted_values) and sorted_values[i] == x else -1


print(find([1, 3, 5, 7], 5), find([1, 3, 5, 7], 4), find([], 1))

# ---- heapq ----
heap = []
for n in [5, 1, 8, 3, 9, 2]:
    heapq.heappush(heap, n)
print(heap[0], [heapq.heappop(heap) for _ in range(6)], heap)
numbers = [9, 4, 7, 1, 8, 2, 6, 3, 5]
heapq.heapify(numbers)
print(numbers, numbers[0], heapq.heappop(numbers), heapq.heappushpop(numbers, 0), heapq.heappushpop(numbers, 4), heapq.heapreplace(numbers, 10), numbers)
print(heapq.nlargest(3, [5, 1, 8, 3, 9, 2]), heapq.nsmallest(3, [5, 1, 8, 3, 9, 2]), heapq.nlargest(0, [1]), heapq.nsmallest(10, [2, 1]))
print(heapq.nlargest(2, ["pear", "fig", "banana", "kiwi"], key=len), heapq.nsmallest(2, ["pear", "fig", "banana", "kiwi"], key=len))
print(list(heapq.merge([1, 4, 7], [2, 5, 8], [3, 6, 9])), list(heapq.merge()), list(heapq.merge([1], [])))
print(list(heapq.merge([7, 4, 1], [8, 2], reverse=True)), list(heapq.merge(["b", "ccc"], ["a", "dd"], key=len)))
tasks = []
heapq.heappush(tasks, (2, "write"))
heapq.heappush(tasks, (1, "plan"))
heapq.heappush(tasks, (3, "ship"))
heapq.heappush(tasks, (1, "check"))
print([heapq.heappop(tasks) for _ in range(len(tasks))])
try:
    heapq.heappop([])
except IndexError as e:
    print("IndexError", e)


def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for _ in range(len(h))]


print(heapsort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]), heapsort("heap"), heapsort([]))
scrambled = [(i * 7919) % 101 for i in range(60)]
print(heapsort(scrambled) == sorted(scrambled), heapq.nsmallest(3, scrambled), heapq.nlargest(3, scrambled))

# ---- time: a date's parts, at UTC (the computer's time zone isn't known here) ----
print(tuple(time.gmtime(0)), time.gmtime(86400 * 365 + 3661)[:6], time.gmtime(1700000000)[:8])
print(len(time.localtime()), len(time.localtime(0)), time.mktime(time.localtime(1700000000)) == 1700000000.0)
