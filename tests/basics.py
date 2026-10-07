# Numbers, strings, variables, control flow.
x = 7
y = 2
print(x + y, x - y, x * y, x / y, x // y, x % y, x ** y)
print(-7 // 2, -7 % 2, 7 // -2, 7 % -2, 2 ** -1, 2 ** 0.5)
print(1.5 + 2, 3.0 * 2, 10 / 4, 1e3, 1e16, 1e-5, 0.1 + 0.2, 1 / 3)
print(7.0 // 2, 7.5 % 2, -7.5 % 2, float("inf"), -float("inf"))
print(0x1F, 0b101, 0o17, 1_000_000)
print(1 < 2 < 3, 1 < 2 > 3, 1 == 1.0, "a" < "b", not True, True and False, True or False)
print(5 & 3, 5 | 3, 5 ^ 3, ~5, 1 << 10, 1024 >> 3)
print(None, True, False, type(1), type("s"), type(1.5), type(None), type([]))
s = "Hello, World"
print(s.upper(), s.lower(), len(s), s[0], s[-1], s[0:5], s[7:], s[::-1], s[::2])
print(s.replace("World", "Python"), s.split(", "), "-".join(["a", "b", "c"]))
print("abc" * 3, "a" + "b", "ell" in s, "xyz" not in s, s.find("o"), s.count("l"))
print("  pad  ".strip() + "|", "x".center(7, "*"), "42".zfill(5), "tEsT".title(), "tEsT".swapcase())
print(repr("it's"), repr('say "hi"'), repr("a\nb"), str(3.0), repr(1.0e100))
if x > 5:
    print("big")
elif x > 2:
    print("medium")
else:
    print("small")
total = 0
for i in range(10):
    if i % 2 == 0:
        continue
    if i > 7:
        break
    total += i
print("total", total)
n = 5
while n > 0:
    n -= 2
else:
    print("while done", n)
for i in range(3):
    pass
else:
    print("for done", i)
for i in range(10, 0, -3):
    print(i, end=" ")
print()
a, b = 1, 2
a, b = b, a
print(a, b)
first, *rest = [1, 2, 3, 4]
*init, last = "abc"
print(first, rest, init, last)
print(1 if a else 2, a or "default", 0 or "default", a and "both", None or 0)
print(abs(-3), abs(-2.5), min(3, 1, 2), max([4, 9, 2]), sum([1, 2, 3]), sum(range(101)))
print(round(2.5), round(3.5), round(2.567, 2), round(-0.5), divmod(17, 5), pow(2, 10), pow(2, 10, 1000))
print(int("42"), int(3.9), int(-3.9), float("2.5"), int("ff", 16), str(42) + "!", bool(0), bool("x"))
print(hex(255), bin(5), oct(8), chr(65), ord("a"), chr(8364))
print(10 ** 18, 2 ** 62, -(2 ** 62))
