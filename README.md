# Adder

A Python interpreter written in [Tessel](https://tessel-lang.netlify.app).
It reads Python source, parses it, and runs it by walking the syntax tree:
no part of CPython is used.

```sh
tessel build . -o adder          # makes ./adder (about 1 MB, nothing else needed)

./adder examples/mandelbrot.py   # run a program
./adder -c "print(sum(range(101)))"
./adder                          # the interactive prompt
```

```
>>> def fib(n):
...     return n if n < 2 else fib(n - 1) + fib(n - 2)
...
>>> [fib(i) for i in range(10)]
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## What it runs

Adder follows Python 3. The programs in `tests/` print exactly what CPython
prints for them, error messages included.

- **Values:** `int`, `float`, `bool`, `str`, `None`, `list`, `tuple`, `dict`,
  `set`, `range`, with their operators, slices, and methods (`str.split`,
  `list.sort`, `dict.setdefault`, `set.union`, …).
- **Statements:** `if`/`elif`/`else`, `while` and `for` (with `else`,
  `break`, `continue`), assignment with unpacking (`a, *rest = xs`),
  augmented assignment, `del`, `assert`, `pass`, `global`, `nonlocal`,
  `with`, `try`/`except`/`else`/`finally`, `raise`.
- **Functions:** defaults, `*args`, `**kwargs`, keyword arguments, closures,
  `lambda`, decorators, recursion, generators (see below).
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

- **Integers are 64-bit.** Python's grow without limit; Adder raises
  `OverflowError` where a result doesn't fit (`2 ** 100`).
- **Generators run all at once.** Calling a function with `yield` runs it to
  its end and keeps what it yielded, so a generator that never ends (`while
  True: yield …`) never returns. `map`, `zip`, `filter` and `enumerate` work
  the same way.
- **Nothing is ever freed.** Adder has no garbage collector: a program that
  makes millions of lists or objects uses more and more memory.
- **Not there:** `async`, `match`, `bytes`, complex numbers, `slice`
  objects, metaclasses, `__slots__`, descriptors of your own, and most of
  the standard library (`collections`, `itertools`, `re`, `datetime`, …).
- A name is looked up where it's used, so reading a variable before the
  function assigns it finds the outer one, where Python raises
  `UnboundLocalError`.
- **Speed:** about a fifth of CPython's on loops and calls.

## How it's made

| File | |
|---|---|
| `lexer.tsl` | Source text to tokens, with `indent` and `dedent` tokens for Python's blocks. |
| `ast.tsl` | The syntax tree: an enum of nodes kept in one list, which name each other by index. |
| `parser.tsl` | A recursive descent parser: a method for each level of Python's grammar. |
| `values.tsl` | Python's values. Lists, dictionaries and objects are shared, not copied, so they live in lists of the interpreter and a value says which one it is. |
| `interp.tsl` | The evaluator: `eval` for expressions, `exec` for statements, calls, and the `signal` that carries `break`, `return` and exceptions outwards. |
| `ops.tsl` | Arithmetic, comparison, `repr`, hashing, attributes, indexing, iteration, classes. |
| `builtins.tsl`, `methods.tsl` | The built-in functions, and the methods of `str`, `list`, `dict`, `set` and files. |
| `format.tsl` | Format specs, `%` formatting and `str.format`. |
| `modules.tsl` | `math`, `random`, `json` and the other modules, and importing files. |
| `main.tsl` | Running a file, `-c`, and the prompt. |

About 10,000 lines of Tessel. Every `.tsl` file in the folder is part of the
program; `tessel.toml` says which version of Tessel builds it.

## Tests

```sh
tessel build . -o adder
tests/run.sh             # each tests/*.py, compared with what CPython prints
tests/run.sh --update    # write the expected output again (needs python3)
```
