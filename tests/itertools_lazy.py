# itertools on iterators that never end: count(), cycle() and repeat(x).
#
# Author: Alexius Academia
# Date: 2026-10-08
#
# This needs generators that run a step at a time. While PyTessel runs a
# generator to its end when it's called, this test can't finish: it's kept
# in tests/pending/, where tests/run.sh doesn't look. Move it to tests/
# (with its .expected) once generators are lazy.
from itertools import (count, cycle, repeat, islice, takewhile, dropwhile, accumulate, chain, compress,
                       filterfalse, starmap, zip_longest, groupby, tee, product)

# count
print(list(islice(count(), 5)))
print(list(islice(count(10), 3)))
print(list(islice(count(1, 2), 5)))
print(list(islice(count(5, -1), 7)))
print(list(islice(count(0.5, 0.25), 4)))
print(list(islice(count(step=3), 4)))
print(list(zip(count(), "abc")))
print(list(zip("abc", count(1))))
print(list(takewhile(lambda n: n < 20, count(0, 7))))
print(next(dropwhile(lambda n: n * n < 500, count())))
c = count(3)
print(next(c), next(c), next(c))
print([n for n in islice(count(), 100) if n % 17 == 0])
print(dict(zip("xyz", count(100, 100))))
print(list(map(lambda a, b: a * b, count(1), [10, 20, 30])))

# cycle
print(list(islice(cycle("AB"), 5)))
print(list(islice(cycle([1, 2, 3]), 7)))
print(list(zip(range(6), cycle(["even", "odd"]))))
print(list(islice(cycle([]), 3)))
print("".join(islice(cycle("abc"), 2, 8)))
colors = cycle(["red", "green"])
print([next(colors) for _ in range(5)])
print(list(islice(cycle(x for x in range(3)), 7)))

# repeat with no times
print(list(islice(repeat("x"), 3)))
print(list(zip(repeat(0), "abc")))
print(list(map(pow, range(5), repeat(2))))
print(list(starmap(pow, zip(repeat(2), range(6)))))

# Never-ending iterators through the other functions.
print(list(islice(accumulate(count(1)), 6)))
print(list(islice(chain("ab", count()), 5)))
print(list(islice(chain.from_iterable(repeat([1, 2])), 5)))
print(list(islice(compress(count(), cycle([1, 0, 0])), 5)))
print(list(islice(filterfalse(lambda n: n % 3, count()), 4)))
print(list(islice(starmap(lambda a, b: a + b, zip(count(), count(10))), 3)))
print(list(islice(zip_longest("ab", count()), 4)))
print([(k, len(list(g))) for k, g in islice(groupby(count(), key=lambda n: n // 4), 3)])
a, b = tee(count())
print(next(a), next(a), next(b), next(a), next(b))
print(list(islice(product(*[range(2)] * 3), 3)))
print(list(islice(islice(count(), 10, None), 3)))
print(list(islice(takewhile(lambda n: True, count()), 2)))


def naturals():
    n = 0
    while True:
        yield n
        n += 1


def primes():
    for n in count(2):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            yield n


print(list(islice(naturals(), 4)), list(islice(primes(), 10)))
print(list(takewhile(lambda p: p < 30, primes())))
