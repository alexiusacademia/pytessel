# PyTessel

A Python interpreter written in [Tessel](https://tessel-lang.netlify.app).
It reads Python source, parses it, and runs it by walking the syntax tree:
no part of CPython is used.

```sh
tessel build . -o pytessel          # makes ./pytessel (about 1 MB, nothing else needed)

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
  `functools.reduce`, `string`; and `import` of other `.py` files next to
  the program.

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
  objects, metaclasses, `__slots__`, descriptors of your own, and most of
  the standard library (`collections`, `itertools`, `re`, `datetime`, …).
- A name is looked up where it's used, so reading a variable before the
  function assigns it finds the outer one, where Python raises
  `UnboundLocalError`.
- **Speed:** about a fifth of CPython's on loops and calls.

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
  `input`, no `os`, no `time.sleep`, no importing files from disk.
- **`budget:`** on `run` and `callFunction` limits how many statements and
  calls may run; past it the Python gets a `TimeoutError` it can't catch
  its way out of.
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

About 12,000 lines of Tessel. Every `.tsl` file in the folder is part of the
program; `tessel.toml` says which version of Tessel builds it.

## Tests

```sh
tessel build . -o pytessel
tests/run.sh             # each tests/*.py, compared with what CPython prints
tests/run.sh --update    # write the expected output again (needs python3)
```
