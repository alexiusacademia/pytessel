# Lists, tuples, dictionaries, sets, comprehensions.
xs = [3, 1, 2]
xs.append(5)
xs.extend([8, 0])
xs.insert(1, 9)
print(xs, len(xs), xs[0], xs[-1], xs[1:3], xs[::-1])
xs.sort()
print(xs, xs.index(5), xs.count(1), 5 in xs)
xs.reverse()
print(xs.pop(), xs.pop(0), xs)
xs.remove(5)
ys = xs
ys.append(100)
print(xs, xs is ys, xs == list(ys), xs is list(ys))
zs = xs[:]
zs[0] = "changed"
xs[1:3] = ["a", "b", "c"]
print(xs, zs)
del xs[0]
del xs[1:3]
print(xs, [1, 2] + [3], [0] * 3, [[1, 2], [3]][0][1])
print(sorted([3, 1, 2], reverse=True), sorted(["bb", "a", "ccc"], key=len), sorted("hello"))
print(list(reversed([1, 2, 3])), list(enumerate("ab")), list(zip([1, 2, 3], "abc")), list(map(str, [1, 2])))
print(list(filter(lambda n: n % 2, range(6))), any([0, 1]), all([1, 0]), list(range(5)), list(range(2, 10, 3)))
t = (1, "two", 3.0)
print(t, t[1], len(t), t + (4,), (1,), (), t.index("two"), 1 in t)
d = {"a": 1, "b": 2}
d["c"] = 3
print(d, d["a"], d.get("z"), d.get("z", 0), "a" in d, len(d))
print(list(d.keys()), list(d.values()), list(d.items()))
for k, v in d.items():
    print(k, v, end="; ")
print()
del d["a"]
print(d.pop("b"), d.pop("nope", "gone"), d, d.setdefault("x", []), d)
d.update({"y": 1}, z=2)
print(d, {**d, "w": 0}, dict(a=1), dict([("k", "v")]), {1: "int", 1.0: "float", True: "bool"})
s = {3, 1, 2, 3}
s.add(4)
s.discard(1)
print(sorted(s), len(s), 2 in s, sorted(s | {9}), sorted(s & {2, 3}), sorted(s - {2}), sorted(s ^ {2, 7}))
print(set(), {1, 2} == {2, 1}, {1} <= {1, 2}, sorted(set("hello")))
print([n * n for n in range(5)], [n for n in range(10) if n % 3 == 0], [(a, b) for a in "ab" for b in (1, 2)])
print({k: len(k) for k in ["a", "bb"]}, sorted({c for c in "banana"}), list(n + 1 for n in range(3)))
print(sum(n for n in range(4)), [[r * c for c in range(3)] for r in range(2)])
matrix = [[1, 2], [3, 4]]
print([row[::-1] for row in matrix], [x for row in matrix for x in row])
nested = {"list": [1, {"deep": (1, 2)}], "set": {1}}
print(nested, nested["list"][1]["deep"][0])
a = [1, 2, 3]
b = a
b += [4]
print(a, a * 2, [1, 2] < [1, 3], (1, 2) == (1, 2), [1, [2, 3]] == [1, [2, 3]])
print("%s has %d items (%.2f%%)" % ("cart", 3, 12.345), "%5d|%-5d|%05d" % (42, 42, 42), "%x %o %e" % (255, 8, 12345.678))
print("{} and {}".format(1, "two"), "{1} {0}".format("a", "b"), "{name!r:>8}".format(name="x"), "{:,}".format(1234567))
