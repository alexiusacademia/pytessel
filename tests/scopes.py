# Where names live: locals, globals, closures, comprehensions, class bodies.


def attempt(f, *args, **kwargs):
    try:
        print(f(*args, **kwargs))
    except Exception as e:
        print(type(e).__name__ + ":", e)


x = "global x"
counter = 0


# ---- a name assigned anywhere in a function is local everywhere in it ----
def read_then_assign():
    print(x)
    x = "local x"
    return x


attempt(read_then_assign)


def assign_then_read():
    x = "local x"
    return x


attempt(assign_then_read)
print(x)


def only_reads():
    return x


attempt(only_reads)


def augmented():
    counter += 1
    return counter


attempt(augmented)


def assigned_in_dead_branch():
    if False:
        x = "never"
    return x


attempt(assigned_in_dead_branch)


def assigned_in_one_branch(flag):
    if flag:
        value = "set"
    return value


attempt(assigned_in_one_branch, True)
attempt(assigned_in_one_branch, False)


def loop_variable(items):
    for item in items:
        pass
    return item


attempt(loop_variable, [1, 2, 3])
attempt(loop_variable, [])


def loop_shadows_global():
    for x in range(3):
        pass
    return x


attempt(loop_shadows_global)
print(x)


def with_target():
    class Manager:
        def __enter__(self):
            return "entered"

        def __exit__(self, *args):
            return False

    before = "unset"
    try:
        before = handle
    except UnboundLocalError as e:
        before = "UnboundLocalError: " + str(e)
    with Manager() as handle:
        pass
    return before, handle


attempt(with_target)


def import_is_local():
    try:
        result = math.pi
    except UnboundLocalError as e:
        result = str(e)
    import math
    return result, math.floor(2.5)


attempt(import_is_local)


def from_import_is_local():
    try:
        result = sqrt(4)
    except UnboundLocalError as e:
        result = str(e)
    from math import sqrt
    return result, sqrt(9)


attempt(from_import_is_local)


def def_is_local():
    try:
        early = helper()
    except UnboundLocalError as e:
        early = str(e)

    def helper():
        return "helped"

    return early, helper()


attempt(def_is_local)


def class_is_local():
    try:
        early = Inner
    except UnboundLocalError as e:
        early = str(e)

    class Inner:
        pass

    return early, Inner.__name__


attempt(class_is_local)


def walrus_is_local():
    try:
        early = w
    except UnboundLocalError as e:
        early = str(e)
    if (w := 10) > 5:
        pass
    return early, w


attempt(walrus_is_local)


def unpacking_is_local():
    try:
        early = b
    except UnboundLocalError as e:
        early = str(e)
    a, (b, *c) = 1, (2, 3, 4)
    return early, a, b, c


attempt(unpacking_is_local)


def parameters_are_local(x, y=2, *rest, key="k", **more):
    x = x + 1
    return x, y, rest, key, more


attempt(parameters_are_local, 1)
attempt(parameters_are_local, 1, 5, 6, 7, key="K", z=1)
print(x)


def attribute_and_item_are_not_names():
    data = {}
    data["x"] = 1
    data["x"] += 1

    class Box:
        pass

    box = Box()
    box.x = 5
    box.x += 1
    return data, box.x, x


attempt(attribute_and_item_are_not_names)


# ---- del ----
def del_then_read():
    value = 1
    del value
    return value


attempt(del_then_read)


def del_unbound():
    del never
    never = 1


attempt(del_unbound)


def del_twice():
    v = 1
    del v
    del v


attempt(del_twice)


def del_then_assign():
    v = 1
    del v
    v = 2
    return v


attempt(del_then_assign)


def del_makes_it_local():
    del x


attempt(del_makes_it_local)
print(x)
module_level = 1
del module_level
try:
    print(module_level)
except NameError as e:
    print("NameError:", e)
try:
    del module_level
except NameError as e:
    print("NameError:", e)
try:
    print(never_defined)
except NameError as e:
    print("NameError:", e, type(e).__name__)
print(issubclass(UnboundLocalError, NameError))


# ---- global ----
def set_global():
    global x, made_here
    old = x
    x = "changed by set_global"
    made_here = "new global"
    return old


attempt(set_global)
print(x, made_here)
x = "global x"


def global_augmented():
    global counter
    counter += 5
    return counter


attempt(global_augmented)
attempt(global_augmented)
print(counter)


def global_read_missing():
    global not_there
    return not_there


attempt(global_read_missing)


def global_del():
    global made_here
    del made_here


attempt(global_del)
try:
    print(made_here)
except NameError as e:
    print("NameError:", e)
attempt(global_del)


def global_skips_enclosing():
    x = "enclosing"

    def inner():
        global x
        return x

    return inner()


attempt(global_skips_enclosing)


def global_in_loop():
    global total
    total = 0
    for i in range(5):
        total += i
    return total


attempt(global_in_loop)
print(total)


# ---- closures and nonlocal ----
def outer_then_inner():
    value = "outer"

    def inner():
        return value

    return inner()


attempt(outer_then_inner)


def free_before_assignment():
    def inner():
        return later

    try:
        result = inner()
    except NameError as e:
        result = type(e).__name__ + ": " + str(e)
    later = "now set"
    return result, inner()


attempt(free_before_assignment)


def free_after_del():
    value = 1

    def inner():
        return value

    del value
    return inner()


attempt(free_after_del)


def inner_shadows():
    value = "outer"

    def inner():
        value = "inner"
        return value

    return inner(), value


attempt(inner_shadows)


def inner_reads_then_assigns():
    value = "outer"

    def inner():
        seen = value
        value = "inner"
        return seen

    return inner()


attempt(inner_reads_then_assigns)


def make_counter():
    count = 0

    def bump(by=1):
        nonlocal count
        count += by
        return count

    def peek():
        return count

    return bump, peek


bump, peek = make_counter()
print(bump(), bump(), bump(10), peek())
other_bump, other_peek = make_counter()
print(other_bump(), peek(), other_peek())


def nonlocal_two_levels():
    level = "top"

    def middle():
        def bottom():
            nonlocal level
            level = "set from bottom"

        bottom()
        return level

    return middle(), level


attempt(nonlocal_two_levels)


def nonlocal_nearest():
    v = "a"

    def middle():
        v = "b"

        def bottom():
            nonlocal v
            v = "c"

        bottom()
        return v

    return middle(), v


attempt(nonlocal_nearest)


def three_levels():
    a = 1

    def two():
        b = 2

        def three():
            c = 3
            return a + b + c + offset

        return three()

    return two()


offset = 100
attempt(three_levels)


def closure_sees_later_value():
    fns = []
    for i in range(3):
        fns.append(lambda: i)
    return [f() for f in fns]


attempt(closure_sees_later_value)


def default_captures_now():
    fns = []
    for i in range(3):
        fns.append(lambda i=i: i)
    return [f() for f in fns]


attempt(default_captures_now)


def default_is_outer_scope(x=x):
    return x


attempt(default_is_outer_scope)


def lambda_scopes():
    y = 5
    f = lambda x: x + y
    g = lambda: undefined_in_lambda
    try:
        g()
    except NameError as e:
        return f(1), str(e)


attempt(lambda_scopes)


def recursion_through_local():
    def fact(n):
        return 1 if n < 2 else n * fact(n - 1)

    return fact(6)


attempt(recursion_through_local)


def generator_locals():
    def gen():
        try:
            yield before
        except UnboundLocalError as e:
            yield str(e)
        before = 1
        yield before
        total = 0
        for i in range(3):
            total += i
            yield total

    return list(gen())


attempt(generator_locals)


def generator_closure():
    base = 10

    def gen(n):
        for i in range(n):
            yield base + i

    g = gen(3)
    first = next(g)
    base = 20
    return first, list(g)


attempt(generator_closure)


# ---- comprehensions have their own variables ----
def comprehension_variable_stays_inside():
    i = "untouched"
    squares = [i * i for i in range(4)]
    return squares, i


attempt(comprehension_variable_stays_inside)
n = "module n"
print([n for n in range(3)], n, {n: n for n in "ab"}, n, {n for n in (1,)}, n, list(n for n in "x"), n)


def comprehension_reads_local():
    factor = 3
    return [factor * v for v in range(3)], {v: factor for v in "ab"}, sum(factor for _ in range(2))


attempt(comprehension_reads_local)


def comprehension_unbound_local():
    try:
        return [v for v in range(3) if unset]
    finally:
        pass
    unset = True


attempt(comprehension_unbound_local)


def genexpr_unbound_free():
    try:
        return list(v for v in range(3) if unset)
    finally:
        pass
    unset = True


attempt(genexpr_unbound_free)


def first_iterable_is_outer():
    items = [1, 2, 3]
    return [items for items in items], items


attempt(first_iterable_is_outer)


def nested_comprehensions():
    rows = [[1, 2], [3, 4]]
    flat = [cell for row in rows for cell in row]
    grid = [[cell * scale for cell in row] for row in rows for scale in (10,)]
    return flat, grid


attempt(nested_comprehensions)


def walrus_in_comprehension():
    seen = [last := v * 2 for v in range(4)]
    return seen, last


attempt(walrus_in_comprehension)


def comprehension_in_closure():
    base = 5

    def inner():
        return [base + v for v in range(3)]

    return inner()


attempt(comprehension_in_closure)


def lambda_in_comprehension():
    fns = [lambda v=v: v * scale for v in range(3)]
    scale = 10
    return [f() for f in fns]


attempt(lambda_in_comprehension)
print([name for name in ("a", "b")], [x for _ in range(2)])
try:
    print([undefined_name for _ in range(1)])
except NameError as e:
    print("NameError:", e)

# ---- class bodies look outward, and aren't seen by their methods ----
kind = "module kind"


class Reads:
    seen = kind
    kind = "class kind"
    again = kind

    def method(self):
        return kind

    def through_self(self):
        return self.kind


print(Reads.seen, Reads.kind, Reads.again, Reads().method(), Reads().through_self())


def class_in_function():
    kind = "function kind"

    class Local:
        seen = kind

        def method(self):
            return kind

    return Local.seen, Local().method()


attempt(class_in_function)


class Scoped:
    limit = 3
    values = list(range(limit))
    doubled = [v * 2 for v in values]

    def method(self):
        try:
            return limit
        except NameError as e:
            return "NameError: " + str(e)


print(Scoped.values, Scoped.doubled, Scoped().method())


class Counter:
    count = 0

    def bump(self):
        Counter.count += 1
        return Counter.count


print(Counter().bump(), Counter().bump(), Counter.count)


# ---- except ... as e is unbound after the block ----
def except_unbinds():
    try:
        raise ValueError("boom")
    except ValueError as e:
        message = str(e)
    try:
        return e
    except UnboundLocalError as err:
        return message, str(err)


attempt(except_unbinds)


def except_unbinds_outer_value():
    e = "kept?"
    try:
        raise KeyError("k")
    except KeyError as e:
        pass
    return e


attempt(except_unbinds_outer_value)


def except_not_taken():
    e = "kept"
    try:
        pass
    except KeyError as e:
        pass
    return e


attempt(except_not_taken)
try:
    raise RuntimeError("module level")
except RuntimeError as err:
    pass
try:
    print(err)
except NameError as e:
    print("NameError:", e)


def except_in_generator():
    def gen():
        try:
            raise ValueError("inside")
        except ValueError as e:
            yield str(e)
        try:
            yield e
        except UnboundLocalError as err:
            yield str(err)

    return list(gen())


attempt(except_in_generator)


def except_keeps_copy():
    try:
        1 / 0
    except ZeroDivisionError as e:
        saved = e
    return type(saved).__name__, str(saved)


attempt(except_keeps_copy)


# ---- match captures are locals too ----
def match_capture(value):
    try:
        early = captured
    except UnboundLocalError as e:
        early = "unbound"
    match value:
        case [captured, *others]:
            return early, captured, others
        case _:
            return early


attempt(match_capture, [1, 2, 3])
attempt(match_capture, 5)


# ---- exec and eval see what's around them ----
def exec_reads_locals():
    local_value = 21
    return eval("local_value * 2"), eval("x")


attempt(exec_reads_locals)
exec("made_by_exec = 7")
print(made_by_exec)
print(sorted(k for k in ("x", "counter", "offset") if k in globals()))


def keyword_only(a, *rest, key=None, flag=False):
    return a, rest, key, flag


attempt(keyword_only, 1, 2, 3)
attempt(keyword_only, 1, key="k")
