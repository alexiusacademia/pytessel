# Exceptions.
def risky(n):
    if n == 0:
        raise ValueError("zero!")
    if n == 1:
        raise KeyError("missing")
    return 10 / (n - 2)

for n in [0, 1, 2, 3]:
    try:
        print("result", risky(n))
    except ValueError as e:
        print("ValueError:", e)
    except (KeyError, IndexError) as e:
        print("lookup:", e, repr(e))
    except ZeroDivisionError as e:
        print("zero division:", e)
    else:
        print("fine")
    finally:
        print("done", n)

class AppError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

try:
    raise AppError("custom", 42)
except Exception as e:
    print(type(e).__name__, e, e.code, e.args, isinstance(e, AppError))

def cleanup():
    try:
        return "try"
    finally:
        print("cleanup runs")

print(cleanup())

for bad in ["[1][5]", "{}['k']", "int('x')", "1 + 'a'", "undefined", "None.x", "len(5)", "'a'.nope()", "[].pop()", "1 / 0", "(1).real()", "assert 1 == 2, 'no'", "next(iter([]))"]:
    try:
        exec(bad) if bad.startswith("assert") else eval(bad)
    except Exception as e:
        print(type(e).__name__ + ":", e)

try:
    try:
        raise RuntimeError("inner")
    except RuntimeError:
        print("handling")
        raise
except RuntimeError as e:
    print("re-raised", e)

try:
    raise TypeError
except TypeError as e:
    print("bare class", repr(e), str(e) == "")

def deep(n):
    return deep(n + 1)
try:
    deep(0)
except RecursionError as e:
    print("RecursionError caught")

try:
    x = [1, 2, 3]
    a, b = x
except ValueError as e:
    print(e)
try:
    a, b, c = [1]
except ValueError as e:
    print(e)
print("still running")
