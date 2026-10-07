# f-strings and formatting.
name = "Ada"
n = 42
pi = 3.14159265
items = ["a", "b"]
d = {"k": 1}
print(f"{name} is {n}", f"{name!r}", f"{n:5}|{n:<5}|{n:^5}|{n:05}|{n:+}|{n:x}|{n:b}|{n:o}|{n:#x}")
print(f"{pi:.2f} {pi:8.3f} {pi:e} {pi:.3e} {pi:g} {1234567.891:,.2f} {0.25:.0%} {1e10:g} {1e-7:g}")
print(f"{name:>10}|{name:<10}|{name:^10}|{name:*^10}|{name:.2}")
print(f"{n + 1} {items[0]} {d['k']} {len(items)} {name.upper()} {'nested'} {n if n > 1 else 0}")
print(f"{{braces}} {n=} {pi=:.2f} {name=}")
w = 8
print(f"{pi:{w}.{2}f}|", f"{1000000:_}", f"{-5:05}", f"{True}", f"{None}", f"{[1, 2]}", f"{(1,)}")
print("{:>6.2f}|{:<6}|{:^6}".format(3.14159, "ab", "c"), format(255, "08b"), format(0.5, ".1%"), format("s", ">3"))
print(str(1e21), str(123456789012345678.0), repr(0.1), 1.0, 100.0, 1e15, 1e16, 123456.789e3, 5e-324, 1.7976931348623157e308)
print(2.5.is_integer(), (3.0).is_integer(), 7 / 2, 7 // 2.0, 2 ** 0.5, 10 ** -2)
text = """line one
  line two
line three"""
print(text.splitlines(), text.count("line"), len(text))
print("a,b,,c".split(","), "  a  b ".split(), "a b c".split(" ", 1), "x".join("abc"), "abc".partition("b"))
print("Hello".startswith(("He", "x")), "Hello".endswith("lo"), "hello world".capitalize(), "x=1".removeprefix("x="))
print("abc".isalpha(), "a1".isalnum(), "12".isdigit(), " ".isspace(), "ABC".isupper(), "abc".islower(), "".isdigit())
print("tab\there", 'single', "double \"quoted\"", r"raw\n", "unié", "é".upper(), len("héllo"), "héllo"[1])
print("abc" < "abd", "Z" < "a", "apple" > "Apple", max("hello"), min("hello"), sorted("bca"), "b" * 0 == "")
print("%s" % 5, "%r" % "s", "%5.1f|" % 2.345, "%-6s|" % "ab", "%03d" % 7, "%%", "%(a)s-%(b)d" % {"a": "x", "b": 2})
print(ascii("x"), str(b"") if False else "skip", "a\\b", len("a\\b"))
