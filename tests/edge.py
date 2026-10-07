# Corners of the language.
print([1, 2, 3][-4:], [1, 2, 3][5:], "abc"[1:100], "abcdef"[-2:], "abcdef"[::-2], [0, 1, 2, 3, 4][1:4:2], list(range(10))[::-3])
xs = list(range(10))
xs[2:5] = []
xs[::2] = ["a"] * 4
print(xs)
del xs[::3]
print(xs, range(5)[2], range(0, 10, 2)[-1], len(range(10, 0, -3)), 5 in range(10), 11 in range(0, 20, 2))
print(True + True, True * 5, sum([True, False, True]), 1 == True, [0, 1][True], {True: "t"}[1], isinstance(True, int))
print(3 == 3.0, hash(3) == hash(3.0), {3: "a"}[3.0], 0.1 + 0.2 == 0.3, 1e308 * 10, -1e308 * 10)
print(7 // 2, -7 // 2, 7 % -3, -7 % 3, 7.5 // 2, divmod(-7, 2), divmod(7.5, 2), 2 ** 3 ** 2, -2 ** 2, (-2) ** 2)
print(1 < 2 == 2, None is None, [] is [], [] == [], "a" in "abc" in ["abc"], not 1 == 2)
print(bool([]), bool([0]), bool(""), bool(" "), bool(0.0), bool(None), bool({}), bool(()), bool(range(0)))
a = b = c = []
a.append(1)
print(b, c is a)
x = y = 5
x += 1
print(x, y)
i = 0
while True:
    i += 1
    if i == 3:
        continue
    if i > 5:
        break
print(i)
for i in range(3):
    for j in range(3):
        if j == 1:
            break
    else:
        print("never")
print(i, j)
def f():
    for i in range(10):
        for j in range(10):
            if i * j == 12:
                return i, j
print(f())
lst = [3, 1, 2]
lst2 = sorted(lst)
lst.sort(reverse=True)
print(lst, lst2, sorted([(2, "b"), (1, "z"), (2, "a")]), sorted(["b", "A", "c"], key=str.lower), sorted([1, 3, 2], key=lambda n: -n))
people = [("bob", 25), ("alice", 30), ("carol", 25)]
print(sorted(people, key=lambda p: p[1]), sorted(people, key=lambda p: p[1], reverse=True), max(people, key=lambda p: p[1]), min(people, key=lambda p: len(p[0])))
d = {}
for word in "the quick the lazy the end".split():
    d[word] = d.get(word, 0) + 1
print(d, max(d, key=d.get), sorted(d.items(), key=lambda kv: (-kv[1], kv[0])))
d2 = {(1, 2): "tuple", 1.5: "float", None: "none", "s": "str"}
print(d2[(1, 2)], d2[None], len(d2), (1, 2) in d2)
try:
    {[1]: 2}
except TypeError as e:
    print(e)
it = iter([1, 2, 3])
print(next(it), list(it), list(it))
print(list(zip("ab", range(5), [True])), dict(zip("abc", range(3))), list(enumerate(["x", "y"], start=1)))
print(isinstance(1, (str, int)), isinstance("s", (int, float)), isinstance(None, type(None)), type(1) == int, type(1) is int, type("") == str)
print(int(True), int("  12  "), int("-0b11", 0), float("1e3"), float(" -2.5 "), str(None), str([1, "a"]), repr("a'b\"c"))
print(max(1, 2.5), min("b", "a"), max([1, 2], [1, 3]), max("abc", key=ord), min([3], default=0), min([], default="empty"))
print(round(1.005, 2), round(2.675, 2), round(1234.5678, -2), round(-2.5), round(0.5), round(1.5), round(7), type(round(1.5)), type(round(1.5, 1)))
print(10 // 3 * 3 + 10 % 3, (5).bit_length(), 255 .bit_length(), abs(-0.0), -0.0 == 0.0, 1_0 + 0x_f)
g = (n * 2 for n in range(3))
print(sum(g), sum(g), list(map(lambda a, b: a + b, [1, 2], [10, 20])))
s = "αβγ"
print(len(s), s[1], s.upper(), s[::-1], [ord(c) for c in s], "日本語".center(7, "*"))
print("a" "b" 'c', "tab:\t|", "nl:\\n", '\x41B', "end")
def gen():
    yield 1
    yield 2
    return
    yield 3
print(list(gen()), [*gen(), *"ab"], {**{"a": 1}, **{"b": 2}}, (*[1, 2], 3))
print(*[1, 2, 3], sep="-")
print("a", "b", sep="", end="!\n")
print()
nums = [1, 2, 3, 4, 5, 6]
evens = [n for n in nums if not n % 2]
print(evens, nums[len(nums) // 2:], nums[:-1], list(reversed(nums))[:2], nums.copy() is nums)
print(globals()["nums"] is nums, "nums" in dir(), callable(len), len.__name__, type(len), type(print).__name__)
print(1 if [] else 2, [] or {} or 0 or "last", 1 and 2 and 3, 0 and 1 / 0, 1 or 1 / 0)
x = 10
def shadow():
    x = 20
    def inner():
        return x
    return inner()
print(shadow(), x)
class K:
    v = [1]
k1, k2 = K(), K()
k1.v.append(2)
k1.w = 0
print(k2.v, hasattr(k2, "w"), K.v is k1.v)
print(chr(ord("a") + 1), "".join(chr(c) for c in range(97, 102)), ord("€"), hex(ord("€")))
print(str(2 ** 62), 9223372036854775807, -9223372036854775808, 4611686018427387904 * 1)
