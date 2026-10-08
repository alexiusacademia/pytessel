# The itertools module, on iterables that end. (The ones that never end,
# count(), cycle() and repeat(x), are in tests/pending/itertools_lazy.py.)
#
# Author: Alexius Academia
# Date: 2026-10-08
import itertools
from itertools import (accumulate, chain, compress, dropwhile, takewhile, filterfalse, groupby, islice,
                       starmap, zip_longest, product, permutations, combinations,
                       combinations_with_replacement, repeat, tee)

# pairwise() came with Python 3.10 and batched() with 3.12: where the
# Python that checks this test is older, it uses these.
try:
    from itertools import pairwise
except ImportError:
    def pairwise(iterable):
        items = list(iterable)
        return iter([(items[i], items[i + 1]) for i in range(len(items) - 1)])
try:
    from itertools import batched
except ImportError:
    def batched(iterable, n):
        if n < 1:
            raise ValueError("n must be at least one")
        items = list(iterable)
        return iter([tuple(items[i:i + n]) for i in range(0, len(items), n)])


def show(label, iterator):
    print(label, list(iterator))


# repeat, with a number of times
show("repeat", repeat("x", 3))
show("repeat 0", repeat(1, 0))
show("repeat kw", repeat([1], times=2))
print(list(map(pow, range(5), repeat(2, 5))))

# accumulate
show("accumulate", accumulate([1, 2, 3, 4, 5]))
show("accumulate mul", accumulate([1, 2, 3, 4, 5], lambda a, b: a * b))
show("accumulate max", accumulate([3, 1, 4, 1, 5, 9, 2], max))
show("accumulate initial", accumulate([1, 2, 3], initial=100))
show("accumulate empty", accumulate([]))
show("accumulate empty initial", accumulate([], initial=7))
show("accumulate str", accumulate("abc"))
show("accumulate func initial", accumulate([1, 2, 3], lambda a, b: a - b, initial=10))

# chain
show("chain", chain("ab", [1, 2], (3,), range(2)))
show("chain none", chain())
show("chain empty", chain([], [], [1]))
show("from_iterable", chain.from_iterable(["ab", "cd", [1]]))
show("from_iterable gen", chain.from_iterable(range(n) for n in range(4)))
print(sum(chain([1, 2], [3, 4])), "".join(chain("ab", "cd")))

# compress, dropwhile, takewhile, filterfalse
show("compress", compress("ABCDEF", [1, 0, 1, 0, 1, 1]))
show("compress short", compress("ABCDEF", [True, True]))
show("dropwhile", dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1]))
show("dropwhile all", dropwhile(lambda x: True, [1, 2]))
show("dropwhile none", dropwhile(lambda x: False, [1, 2]))
show("takewhile", takewhile(lambda x: x < 5, [1, 4, 6, 4, 1]))
show("takewhile all", takewhile(lambda x: True, [1, 2]))
show("takewhile none", takewhile(lambda x: False, [1, 2]))
show("filterfalse", filterfalse(lambda x: x % 2, range(10)))
show("filterfalse None", filterfalse(None, [0, 1, "", "a", [], [0], None]))

# groupby
print([(k, list(g)) for k, g in groupby("AAAABBBCCDAABBB")])
print([(k, len(list(g))) for k, g in groupby([1, 1, 2, 3, 3, 3, 1])])
print([(k, list(g)) for k, g in groupby(["apple", "avocado", "banana", "blueberry", "cherry"], key=lambda w: w[0])])
print([(k, list(g)) for k, g in groupby([])])
print([(k, [x for x in g]) for k, g in groupby(range(10), key=lambda n: n // 3)])
people = [("ann", 30), ("bob", 25), ("cat", 30), ("dan", 25)]
for age, group in groupby(sorted(people, key=lambda p: p[1]), key=lambda p: p[1]):
    print(age, [name for name, _ in group])
print([k for k, g in groupby("aabbccaa")], ["".join(g) for k, g in groupby("aabbccaa")])

# islice
show("islice stop", islice("ABCDEFG", 2))
show("islice start stop", islice("ABCDEFG", 2, 4))
show("islice start None", islice("ABCDEFG", 2, None))
show("islice step", islice("ABCDEFG", 0, None, 2))
show("islice all", islice("ABCDEFG", 1, 6, 2))
show("islice zero", islice("ABCDEFG", 0))
show("islice past end", islice([1, 2, 3], 10))
show("islice empty range", islice(range(10), 5, 2))
show("islice None stop", islice(range(5), None))
show("islice None start", islice(range(10), None, 3))
show("islice big step", islice(range(10), 1, None, 4))
for bad in [(-1,), (1, -1), (0, 5, 0), (0, 5, -1), ("a",)]:
    try:
        list(islice(range(10), *bad))
    except ValueError as e:
        print("ValueError", e)

# pairwise, starmap
show("pairwise", pairwise("ABCD"))
show("pairwise one", pairwise([1]))
show("pairwise none", pairwise([]))
print([b - a for a, b in pairwise([1, 4, 9, 16, 25])])
show("starmap", starmap(pow, [(2, 5), (3, 2), (10, 3)]))
show("starmap lambda", starmap(lambda a, b=10: a + b, [(1,), (1, 2)]))
show("starmap none", starmap(pow, []))

# zip_longest
show("zip_longest", zip_longest("ABCD", "xy"))
show("zip_longest fill", zip_longest("ABCD", "xy", fillvalue="-"))
show("zip_longest three", zip_longest([1], [1, 2], [1, 2, 3], fillvalue=0))
show("zip_longest none", zip_longest())
show("zip_longest one", zip_longest("ab"))
show("zip_longest same", zip_longest("ab", "cd"))
show("zip_longest empty", zip_longest([], [1, 2]))

# product
show("product", product("AB", "xy"))
show("product repeat", product(range(2), repeat=3))
show("product three", product([1, 2], "a", (True, False)))
show("product none", product())
show("product empty", product([1, 2], []))
show("product repeat 0", product("ab", repeat=0))
show("product two repeat", product("ab", [1], repeat=2))
print(len(list(product(range(4), repeat=4))), sum(a * b for a, b in product(range(5), range(5))))
try:
    product("ab", repeat=-1)
except ValueError as e:
    print("ValueError", e)

# permutations
show("permutations", permutations("ABC"))
show("permutations 2", permutations("ABCD", 2))
show("permutations range", permutations(range(3)))
show("permutations 0", permutations("AB", 0))
show("permutations too many", permutations("AB", 3))
show("permutations empty", permutations([]))
print(len(list(permutations(range(6)))), len(list(permutations(range(6), 3))))
print(["".join(p) for p in permutations("abc")])
try:
    permutations("ab", -1)
except ValueError as e:
    print("ValueError", e)

# combinations
show("combinations", combinations("ABCD", 2))
show("combinations 3", combinations(range(4), 3))
show("combinations all", combinations("ABC", 3))
show("combinations 0", combinations("ABC", 0))
show("combinations too many", combinations("AB", 3))
show("combinations 1", combinations([5, 6, 7], 1))
print(len(list(combinations(range(10), 4))), sum(1 for c in combinations(range(8), 3) if sum(c) % 2 == 0))
try:
    combinations("ab", -1)
except ValueError as e:
    print("ValueError", e)

# combinations_with_replacement
show("cwr", combinations_with_replacement("ABC", 2))
show("cwr 3", combinations_with_replacement([0, 1], 3))
show("cwr 0", combinations_with_replacement("AB", 0))
show("cwr empty", combinations_with_replacement([], 2))
show("cwr empty 0", combinations_with_replacement([], 0))
print(len(list(combinations_with_replacement(range(5), 3))))
try:
    combinations_with_replacement("ab", -2)
except ValueError as e:
    print("ValueError", e)

# batched
show("batched", batched("ABCDEFG", 3))
show("batched even", batched(range(6), 2))
show("batched one", batched([1, 2, 3], 1))
show("batched big", batched([1, 2, 3], 10))
show("batched none", batched([], 2))
try:
    batched("abc", 0)
except ValueError as e:
    print("ValueError", e)

# tee
a, b = tee([1, 2, 3])
print(list(a), list(b))
a, b, c = tee(iter("xyz"), 3)
print(next(a), next(a), next(b), list(c), list(a), list(b))
print(len(tee([1, 2], 0)), [list(t) for t in tee(range(3), 4)])
first, second = tee(x * x for x in range(5))
print(sum(first), max(second))

# One after the other, and inside each other.
print(list(islice(chain.from_iterable(repeat([1, 2, 3], 3)), 2, 7)))
print(list(starmap(lambda a, b: a + b, zip_longest([1, 2, 3], [10, 20], fillvalue=0))))
print(sorted(set("".join(p) for p in permutations("aab"))))
print([list(g) for k, g in groupby(accumulate([1, 0, 0, 2, 0, 3]))])
print(list(takewhile(lambda p: p[0] < 2, product(range(3), "ab"))))
print(list(compress(range(10), chain([1, 0] * 3, repeat(1, 4)))))
print(dict(zip_longest("abc", range(2))))
print(list(accumulate(chain([1], [2, 3]), initial=0)))
print([sum(c) for c in combinations([1, 2, 3, 4], 2)])
print(list(filterfalse(lambda t: t[0] == t[1], product("ab", repeat=2))))
print(max(permutations([1, 2, 3])), min(combinations("dcba", 2)))
deck = list(product("AK", "SH"))
print(deck, len(list(combinations(deck, 2))))

# They're iterators: next() takes one item at a time.
it = chain([1], [2])
print(next(it), next(it), next(it, "done"))
it = islice(range(100), 3)
print(next(it), list(it), list(it))
it = accumulate([5, 5])
print(iter(it) is it, next(it), next(it))
try:
    next(it)
except StopIteration:
    print("StopIteration")
print(itertools.chain is chain, hasattr(itertools, "count"), hasattr(itertools, "cycle"))
