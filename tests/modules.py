# The built-in modules.
import math
import json
import sys
import os
import os.path
from functools import reduce
from math import sqrt, pi as PI, floor
import random as rnd
import string

print(math.sqrt(16), sqrt(2), PI, math.e, math.floor(-2.5), math.ceil(2.1), floor(7.9), math.trunc(-2.7))
print(math.factorial(10), math.gcd(12, 18), math.pow(2, 8), math.log(math.e), math.log10(1000), math.log2(8), math.log(8, 2))
print(round(math.sin(math.pi / 2), 6), round(math.cos(0), 6), round(math.atan2(1, 1), 6), math.hypot(3, 4), math.degrees(math.pi))
print(math.isnan(float("nan")), math.isinf(math.inf), math.inf > 10 ** 18, math.isqrt(17), math.fabs(-2), math.comb(5, 2), math.prod([1, 2, 3, 4]))
print(math.isclose(0.1 + 0.2, 0.3), math.copysign(3, -1), math.fmod(-7, 3), math.radians(180) == math.pi, math.tau)
try:
    math.sqrt(-1)
except ValueError as e:
    print("ValueError:", e)
data = {"name": "Ada", "tags": ["x", "y"], "n": 1.5, "ok": True, "none": None, "nested": {"a": [1, 2, {"b": "c"}]}}
text = json.dumps(data)
print(text)
print(json.dumps(data, indent=2))
print(json.dumps([1, "two", 3.0, False, None]), json.dumps("quote\"s\n"), json.dumps({"b": 1, "a": 2}, sort_keys=True))
back = json.loads(text)
print(back == data, back["nested"]["a"][2]["b"], json.loads("[1, 2.5, \"x\", true, null, {\"k\": []}]"), json.loads('"\\u00e9"'))
print(reduce(lambda a, b: a * b, range(1, 6)), reduce(lambda a, b: a + b, [], 10))
print(string.ascii_lowercase[:5], string.digits, len(string.ascii_letters))
print(type(sys.argv), sys.maxsize, os.path.join("a", "b", "c.txt"), os.path.basename("/x/y/z.py"), os.path.dirname("/x/y/z.py"), os.path.splitext("a/b.tar.gz"))
print(os.path.exists("modules.py"), os.path.exists("nope.txt"), os.path.isdir("."), os.path.isfile("modules.py"))
r = rnd.random()
i = rnd.randint(1, 6)
c = rnd.choice(["a", "b", "c"])
xs = list(range(10))
rnd.shuffle(xs)
print(0 <= r < 1, 1 <= i <= 6, c in "abc", sorted(xs) == list(range(10)), len(rnd.sample(range(100), 5)), 3 <= rnd.uniform(3, 4) <= 4, rnd.randrange(10) < 10)
try:
    import nonexistent_module
except ImportError as e:
    print(type(e).__name__, e)
import helper
from helper import double, CONSTANT as K
print(helper.triple(4), double(21), K, helper.Shape(3).area(), helper.__name__)
