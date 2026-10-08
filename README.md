# PyTessel

A Python interpreter written in [Tessel](https://tessel-lang.netlify.app).
It reads Python source, parses it, and runs it by walking the syntax tree:
no part of CPython is used.

```sh
tessel build . -o pytessel          # makes ./pytessel (under 3 MB, nothing else needed)

./pytessel examples/mandelbrot.py   # run a program
./pytessel -c "print(sum(range(101)))"
./pytessel                          # the interactive prompt
```

```
>>> def fib(n):
...     return n if n < 2 else fib(n - 1) + fib(n - 2)
...
>>> [fib(i) for i in range(10)]
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## What it runs

PyTessel follows Python 3. The programs in `tests/` print exactly what CPython
prints for them, error messages included.

- **Values:** `int`, `float`, `bool`, `str`, `None`, `list`, `tuple`, `dict`,
  `set`, `range`, with their operators, slices, and methods (`str.split`,
  `list.sort`, `dict.setdefault`, `set.union`, …).
- **Statements:** `if`/`elif`/`else`, `while` and `for` (with `else`,
  `break`, `continue`), assignment with unpacking (`a, *rest = xs`),
  augmented assignment, `del`, `assert`, `pass`, `global`, `nonlocal`,
  `with`, `try`/`except`/`else`/`finally`, `raise`.
- **Functions:** defaults, `*args`, `**kwargs`, keyword arguments, closures,
  `lambda`, decorators, recursion.
- **Generators:** a function with `yield` runs up to its next `yield` each
  time it's asked for a value, so one that never ends (`while True: yield
  …`) is fine; `send`, `throw`, `close`, `yield from` and generator
  expressions. `map`, `filter`, `zip`, `enumerate`, `reversed` and `iter` give
  a value at a time too, and so do your own classes with `__iter__` and
  `__next__`.
- **Classes:** inheritance (several bases too), `super()`, properties with
  setters, `staticmethod`, `classmethod`, and the special methods: `__init__`,
  `__repr__`, `__str__`, `__eq__`, `__lt__`, `__add__` and the other
  operators, `__len__`, `__getitem__`, `__contains__`, `__iter__`,
  `__next__`, `__call__`, `__bool__`, `__hash__`, `__enter__`, `__exit__`.
- **Expressions:** comprehensions (list, dict, set, generator), f-strings
  with format specs (`f"{price:>10,.2f}"`, `f"{x=}"`), `%` formatting,
  `str.format`, chained comparisons, `x if c else y`, `:=`.
- **Exceptions:** the built-in ones (`ValueError`, `KeyError`, …), your own
  classes, tracebacks for the ones nothing catches.
- **Built-in functions:** `print`, `len`, `range`, `sorted`, `enumerate`,
  `zip`, `map`, `filter`, `sum`, `min`, `max`, `isinstance`, `open`,
  `input`, `eval`, `exec`, and the rest of the usual ones.
- **Modules:** `math`, `random`, `time`, `json`, `sys`, `os`, `os.path`,
  `string`, and the ones under [The standard library](#the-standard-library):
  `datetime`, `re`, `collections`, `itertools`, `functools`, `statistics`,
  `operator`, `copy`, `textwrap`, `bisect`, `heapq`; and `import` of other
  `.py` files next to the program.

## What it doesn't

- **Integers are 64-bit.** Python's grow without limit; PyTessel raises
  `OverflowError` where a result doesn't fit (`2 ** 100`).
- **`yield` inside a larger expression.** `yield` is understood where it's
  nearly always written: as a statement (`yield v`, `yield from g`) or as
  the whole right side of an assignment or a `return` (`x = yield v`,
  `x += yield v`, `x = yield from g`, `return (yield v)`). Anywhere else
  (`print((yield))`, `if (yield v):`, `[(yield a), (yield b)]`) it raises a
  `SyntaxError` when the generator gets there.
- **Nothing is ever freed.** PyTessel has no garbage collector: a program that
  makes millions of lists or objects uses more and more memory. And a
  generator that's dropped half way doesn't run its `finally` blocks, as
  Python does when it frees one: only `close()` does, or leaving (`break`,
  `return`) a `for` loop that called the generator function itself
  (`for x in lines(): … break`).
- **Not there:** `async`, `match`, `bytes`, complex numbers, `slice`
  objects, metaclasses, `__slots__`, descriptors of your own, classes that
  inherit from `dict`, `list` or `tuple`, and the rest of the standard
  library (`enum`, `decimal`, `fractions`, `pathlib`, `csv`, …).
- A name is looked up where it's used, so reading a variable before the
  function assigns it finds the outer one, where Python raises
  `UnboundLocalError`.
- **Speed:** about a fifth of CPython's on loops and calls.

## The standard library

These modules come with PyTessel: `import` finds them with no file, in a
sandbox too. They do what CPython's do for the parts listed, error messages
included. (They show themselves as Python 3.9 does where versions differ:
`OrderedDict([('a', 1)])`.)

| Module | What it has | What's missing |
|---|---|---|
| `datetime` | `date`, `time`, `datetime`, `timedelta`, `timezone` and `tzinfo`: making them (with the checks), `today`, `now`, `fromisoformat`, `fromordinal`, `fromtimestamp`, `fromisocalendar`, `combine`, `replace`, `weekday`, `isocalendar`, `timestamp`, `astimezone`, arithmetic and comparison, `isoformat`, `strftime`, `strptime`, hashing, `min`/`max`/`resolution` | Named time zones (`zoneinfo`): the computer's own zone and fixed distances from UTC are all there is. `timetuple()` gives a plain tuple. `strptime` has no `%U %W %G %V`. A timedelta of more than about 290,000 years can't be divided or multiplied by a float. `fromisoformat` reads what `isoformat` writes, as Python 3.9's does. |
| `re` | `compile`, `match`, `search`, `fullmatch`, `findall`, `finditer`, `sub`, `subn`, `split`, `escape`, `purge`, `error`; Pattern and Match objects; sets, groups (named too), back references, greedy and lazy quantifiers, lookahead, lookbehind of a fixed width, `^ $ \A \Z \b \B`, the flags `I M S X A` and `(?i)`, `(?i:…)` | Conditional groups `(?(1)…)`, `\N{name}`, `re.LOCALE`, `re.DEBUG`, patterns of `bytes`. `\d` is ASCII's digits; which characters are letters, outside ASCII, is known roughly. A group inside `(?!…)` is never set. A repeat is written out as many times as it says, so `a{100000}` (and any pattern that comes to more than 200,000 steps) is refused. |
| `collections` | `Counter`, `defaultdict`, `OrderedDict`, `deque`, `namedtuple`, `ChainMap` | They aren't `dict`s or `tuple`s to `isinstance`, to `json.dumps` or to `**` (`dict(counter)` makes one). A named tuple has no slices (`p[0:2]`), and as a dictionary key it isn't the same key as the plain tuple. `UserDict`, `UserList`, `UserString`, `collections.abc`. |
| `itertools` | `count`, `cycle`, `repeat`, `accumulate`, `chain`, `chain.from_iterable`, `compress`, `dropwhile`, `takewhile`, `filterfalse`, `groupby`, `islice`, `pairwise`, `starmap`, `zip_longest`, `product`, `permutations`, `combinations`, `combinations_with_replacement`, `batched`, `tee` | The ones that never end, until generators run a step at a time (see above). `product` works its whole result out first. |
| `functools` | `reduce`, `partial`, `lru_cache`, `cache`, `wraps`, `update_wrapper`, `cmp_to_key`, `total_ordering` | `singledispatch`, `cached_property`, `partialmethod`. |
| `statistics` | `mean`, `fmean`, `geometric_mean`, `median`, `median_low`, `median_high`, `mode`, `multimode`, `variance`, `pvariance`, `stdev`, `pstdev`, `StatisticsError` | `Fraction` and `Decimal` data, `harmonic_mean`, `quantiles`, `median_grouped`, `NormalDist`. Python adds with exact fractions; PyTessel adds without loss and corrects its divisions, which gives the same floats but, rarely, for the last digit. |
| `operator` | The operators as functions (`add`, `lt`, `getitem`, `iadd`, …), `itemgetter`, `attrgetter`, `methodcaller` | `matmul`. `itemgetter` with a slice. |
| `copy` | `copy`, `deepcopy` (with `__copy__` and `__deepcopy__`) | `__reduce__` and the pickling methods. |
| `textwrap` | `wrap`, `fill`, `shorten`, `dedent`, `indent`, `TextWrapper` | |
| `bisect`, `heapq` | All of both | `heapq.merge` sorts everything at once. |
| `time` | `time`, `sleep`, `perf_counter`, `monotonic`, `process_time`, `time_ns`, `localtime`, `gmtime`, `mktime` | `strftime`, `strptime`; `localtime` and `gmtime` give plain tuples. |

`enum` isn't there: `Color.RED`, `Color(1)`, `Color["RED"]` and `for c in
Color` all need a class to say what calling, indexing and looping over
*the class itself* do, which takes a metaclass.

Most of them are written in Python, in `lib/`: PyTessel carries their text
inside itself (`stdlib.tsl`) and runs it the first time a module is
imported. `re`'s engine is in Tessel (`regex.tsl`). After changing a file
of `lib/`:

```sh
tools/make-stdlib.sh         # writes stdlib.tsl again (needs python3)
tessel build . -o pytessel
```

A `.py` file next to the program with the name of one of these modules is
imported instead of it, as in Python.

## Inside another program

PyTessel can run inside a Tessel program, as a module. Copy every `.tsl`
file except `main.tsl` into a folder of the program (say `python/`) and
import it; `embed.tsl` is the way in:

```
import python

var py = python.newSession()                 // in a sandbox, by default
let r = python.run(py, "def double(x):\n    return x * 2\n")
let c = python.callFunction(py, "double", [.int(i: 21)])   // c.value is .int(i: 42)
```

- **`run`** runs a text in the session (what it defines stays) and gives
  back what it printed and, if it failed, the error, its line and the
  traceback. **`callFunction`** calls a function the Python defined, with
  `HostValue`s (none, bool, int, float, str, list). **`functions`** lists
  them with their parameters.
- **The sandbox** (on unless `newSession(sandbox: false)`): no `open`, no
  `input`, no `os`, no `time.sleep`, no importing files from disk (the
  modules of the standard library aren't files: they're there).
- **`budget:`** on `run` and `callFunction` limits how many statements and
  calls may run; past it the Python gets a `TimeoutError` it can't catch
  its way out of. A regular expression that goes on and on is stopped by
  it too. Importing a module of the standard library costs nothing.
- **`addModule(session, name, source)`** gives the Python a module as text
  for `import name`.
- **The host:** a struct of the program that conforms to `python.Host`,
  set with `setHost`, answers `__host__("name", …)` calls made in Python;
  `hostOf(session) as? YourHost` gives it back with what it changed.
- A `Session` is a value: copy it, run something in the copy, throw the
  copy away.

## How it's made

| File | |
|---|---|
| `lexer.tsl` | Source text to tokens, with `indent` and `dedent` tokens for Python's blocks. |
| `ast.tsl` | The syntax tree: an enum of nodes kept in one list, which name each other by index. |
| `parser.tsl` | A recursive descent parser: a method for each level of Python's grammar. |
| `values.tsl` | Python's values. Lists, dictionaries and objects are shared, not copied, so they live in lists of the interpreter and a value says which one it is. |
| `interp.tsl` | The evaluator: `eval` for expressions, `exec` for statements, calls, and the `signal` that carries `break`, `return` and exceptions outwards. |
| `iterators.tsl` | Iteration, a value at a time: `getIter` and `nextValue`, which every loop and every `zip`, `map`, `next`, `in`, … goes through, and generator expressions. |
| `generators.tsl` | Generators (see below). |
| `ops.tsl` | Arithmetic, comparison, `repr`, hashing, attributes, indexing, classes. |
| `builtins.tsl`, `methods.tsl` | The built-in functions, and the methods of `str`, `list`, `dict`, `set` and files. |
| `format.tsl` | Format specs, `%` formatting and `str.format`. |
| `modules.tsl` | `math`, `random`, `json` and the other modules, and importing files. |
| `regex.tsl` | Regular expressions: a pattern becomes a small program, which a machine that backtracks runs against a text. |
| `stdlib.tsl` | The text of the modules of `lib/`, made by `tools/make-stdlib.sh`. |
| `lib/*.py` | The standard library's modules that are written in Python. |
| `embed.tsl` | A new interpreter, and PyTessel inside another program: sessions, the sandbox, the host. |
| `main.tsl` | Running a file, `-c`, and the prompt. |

**Generators.** The evaluator runs a statement by calling itself for the
statements inside it, and a call can't be left half way and gone back into
later. So a generator's body runs another way. The parser marks every
statement that has a `yield` somewhere inside it. A generator keeps its own
variables and a stack of frames, one for each block it's inside of (the
function's body, a loop's, a `try`'s, a `with`'s), each with how far it has
got, the loop's iterator, or what was on its way out when a `finally` began.
A statement with no `yield` in it is run whole by the evaluator, as anywhere
else; a marked one is opened into a frame of its own; and at the `yield`
itself the generator stops, and gives the value. The next `next` or `send`
goes on from the frames as they were left: what's sent becomes the `yield`'s
value, and `throw` and `close` raise an exception there instead.

About 14,500 lines of Tessel, and 4,800 of Python in `lib/`. Every `.tsl`
file in the folder is part of the program; `tessel.toml` says which version
of Tessel builds it.

## Tests

```sh
tessel build . -o pytessel
tests/run.sh             # each tests/*.py, compared with what CPython prints
tests/run.sh --update    # write the expected output again (needs python3)
```
