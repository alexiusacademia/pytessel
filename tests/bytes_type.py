# bytes and bytearray.
import os


def attempt(f):
    try:
        print(f())
    except Exception as e:
        print(type(e).__name__ + ":", e)


# ---- literals and repr ----
print(b"abc", b'abc', b"", b'')
print(b"it's", b'say "hi"', b"both ' and \"")
print(b"tab\there", b"line\nbreak", b"cr\r", b"back\\slash")
print(b"\x00\x01\x7f\x80\xff", b"\x41\x42", b"\101\102\0", b"\7")
print(rb"raw\n\x41", Rb"\d+", bR'\\', br"it's")
print(b"one" b"two" b' three')
print(b"A stays")
print(repr(b"abc"), str(b"abc"), [b"a", b"b"], (b"\xff",), {b"k": b"v"})
print(b"""several
lines""")
print(len(b"abc"), len(b""), len(b"\x00\x00"))
print(type(b"a"), type(bytearray()), type(b"a").__name__, bytes, bytearray)
print(isinstance(b"a", bytes), isinstance(b"a", str), isinstance(bytearray(b"a"), bytes),
      isinstance(bytearray(b"a"), bytearray), isinstance(b"a", (str, bytes)))
print(bool(b""), bool(b"\x00"), bool(bytearray()), bool(bytearray(1)))
print("yes" if b"x" else "no", "yes" if b"" else "no")

# ---- making them ----
print(bytes(), bytes(3), bytes([65, 66, 67]), bytes((0, 255)), bytes(range(5)))
print(bytes("héllo", "utf-8"), bytes("abc", "ascii"), bytes("é", "latin-1"), bytes("abc", encoding="utf-8"))
print(bytes(b"copy"), bytes(bytearray(b"from array")), bytes(x * 2 for x in range(4)), bytes({7}))
print(bytearray(), bytearray(2), bytearray([1, 2, 3]), bytearray(b"abc"), bytearray("hi", "utf-8"))
attempt(lambda: bytes("abc"))
attempt(lambda: bytes([256]))
attempt(lambda: bytes([-1]))
attempt(lambda: bytes(["a"]))
attempt(lambda: bytes(-1))
attempt(lambda: bytes(1.5))
attempt(lambda: bytes(None))
attempt(lambda: bytearray("abc"))
attempt(lambda: bytearray([300]))
attempt(lambda: bytearray(2.5))
attempt(lambda: bytes(3, "utf-8"))
attempt(lambda: bytes("abc", "klingon"))


class Packed:
    def __bytes__(self):
        return b"packed!"


print(bytes(Packed()))

# ---- encode and decode ----
print("hello".encode(), "héllo wörld €".encode("utf-8"), "日本語".encode(), "😀".encode())
print("abc".encode("ascii"), "café".encode("latin-1"), "abc".encode("UTF8"), "abc".encode("Latin_1"))
print(b"hello".decode(), b"h\xc3\xa9llo".decode("utf-8"), b"\xe6\x97\xa5\xe6\x9c\xac".decode(),
      b"\xf0\x9f\x98\x80".decode() == "😀")
print(b"caf\xe9".decode("latin-1"), b"abc".decode("ascii"), b"abc".decode(encoding="utf-8"))
print("héllo".encode().decode() == "héllo", "€".encode("utf-8").hex(), len("€".encode()))
print(str(b"abc", "utf-8"), str(b"caf\xe9", "latin-1"), str(b"abc", encoding="ascii"), str(bytearray(b"xyz"), "ascii"))
attempt(lambda: "café".encode("ascii"))
attempt(lambda: "ab€£".encode("ascii"))
attempt(lambda: "a€b".encode("latin-1"))
attempt(lambda: "😀".encode("latin-1"))
print("café".encode("ascii", "ignore"), "café".encode("ascii", "replace"), "a€b".encode("latin-1", errors="replace"))
attempt(lambda: b"\xff".decode())
attempt(lambda: b"ab\x80cd".decode("utf-8"))
attempt(lambda: b"\xc3".decode())
attempt(lambda: b"\xe4\xb8".decode())
attempt(lambda: b"\xe4\x41\x42".decode())
attempt(lambda: b"\xe4\xb8\x41".decode())
attempt(lambda: b"\xc0\xaf".decode())
attempt(lambda: b"\xed\xa0\x80".decode())
attempt(lambda: b"\xf5\x80\x80\x80".decode())
attempt(lambda: b"abc\xe9".decode("ascii"))
print(b"a\xffb".decode("utf-8", "ignore"), b"a\xffb".decode("utf-8", "replace") == "a�b",
      b"a\xe4\xb8b".decode(errors="replace") == "a�b", b"x\xe9y".decode("ascii", "ignore"),
      b"x\xe9y".decode("ascii", "replace") == "x�y")
attempt(lambda: "abc".encode("nope"))
attempt(lambda: b"abc".decode("nope"))
attempt(lambda: "abc".encode("utf-8", "sometimes"))
attempt(lambda: "abc".encode(1))
attempt(lambda: str(5, "utf-8"))
try:
    b"\xff".decode()
except UnicodeDecodeError as e:
    print("caught", isinstance(e, UnicodeError), isinstance(e, ValueError))
try:
    "é".encode("ascii")
except UnicodeEncodeError as e:
    print("caught", isinstance(e, UnicodeError), isinstance(e, ValueError))

# ---- indexing, slicing, iteration ----
data = b"hello world"
print(data[0], data[-1], data[4], type(data[0]))
print(data[:5], data[6:], data[::2], data[::-1], data[2:-2], data[100:], data[-3:])
print(type(data[1:3]), bytearray(b"abcdef")[1:4], type(bytearray(b"abcdef")[1:4]))
print(list(b"abc"), [x for x in b"\x00\xff"], tuple(bytearray(b"hi")), sum(b"\x01\x02\x03"))
for b in b"AZ":
    print(b, chr(b), end=" | ")
print()
print(sorted(b"hello"), max(b"hello"), min(b"hello"), list(reversed(b"abc")), list(enumerate(b"ab")))
it = iter(b"xy")
print(next(it), next(it), next(it, "done"))
a, b, c = b"abc"
print(a, b, c)
first, *rest = b"wxyz"
print(first, rest)
attempt(lambda: b"abc"[3])
attempt(lambda: b"abc"[-4])
zero = "0"
half = 1.0
attempt(lambda: b"abc"[zero])
attempt(lambda: bytearray(b"abc")[10])
attempt(lambda: bytearray(b"abc")["x"])
attempt(lambda: b"abc"[half])

# ---- membership ----
print(97 in b"abc", 100 in b"abc", b"bc" in b"abc", b"cb" in b"abc", b"" in b"abc", b"a" not in b"abc")
print(bytearray(b"b") in b"abc", b"lo w" in bytearray(b"hello world"), 0 in bytearray(3))
attempt(lambda: "a" in b"abc")
attempt(lambda: 256 in b"abc")
attempt(lambda: b"a" in "abc")
attempt(lambda: 1.5 in b"abc")

# ---- concatenation, repetition, comparison ----
print(b"ab" + b"cd", b"ab" * 3, 2 * b"xy", b"ab" * 0, b"ab" * -1, b"" + b"")
print(b"a" + bytearray(b"b"), bytearray(b"a") + b"b", type(b"a" + bytearray(b"b")), type(bytearray(b"a") + b"b"))
print(b"abc" == b"abc", b"abc" == b"abd", b"abc" != b"abc", b"abc" == bytearray(b"abc"), bytearray(b"x") == bytearray(b"x"))
print(b"abc" == "abc", "abc" == b"abc", b"abc" != "abc", b"a" == 97, b"" == "", b"abc" == [97, 98, 99])
print(b"abc" < b"abd", b"abc" < b"ab", b"ab" < b"abc", b"abc" <= b"abc", b"b" > b"abc", b"abc" >= b"abd",
      b"a" < bytearray(b"b"), b"\xff" > b"\x7f")
print(sorted([b"pear", b"apple", b"fig", b""]), max(b"aa", b"ab"), min([b"b", b"a"]))
attempt(lambda: b"abc" + "def")
attempt(lambda: "abc" + b"def")
attempt(lambda: bytearray(b"abc") + "def")
attempt(lambda: b"abc" + 1)
attempt(lambda: b"abc" < "abd")
attempt(lambda: b"abc" * 1.5)
attempt(lambda: b"abc" * b"x")
attempt(lambda: b", ".join(["a", "b"]))
attempt(lambda: ", ".join([b"a", b"b"]))
attempt(lambda: "abc".startswith(b"a"))
attempt(lambda: b"abc".startswith("a"))
attempt(lambda: b"abc".find("b"))
attempt(lambda: b"abc".replace("a", "b"))
attempt(lambda: b"a b".split(" "))
attempt(lambda: "a b".split(b" "))
attempt(lambda: b"abc".strip("a"))
attempt(lambda: len(b"abc" + None))

# ---- hashing ----
table = {b"key": 1, b"other": 2, "key": 3}
print(table[b"key"], table["key"], table[bytes([107, 101, 121])], len(table), b"other" in table, b"none" in table)
table[b"key"] += 10
print(table)
print(len({b"a", b"a", b"b", "a"}), hash(b"abc") == hash(b"abc"), hash(b"abc") == hash(bytes(b"abc")))
attempt(lambda: {bytearray(b"a"): 1})
attempt(lambda: hash(bytearray(b"a")))
attempt(lambda: {bytearray(b"a")})

# ---- methods ----
print(b"\x00\xff\x10".hex(), bytearray(b"AB").hex(), b"".hex(), b"\x01\x02\x03".hex(":"), b"\xde\xad".hex("-"))
print(bytes.fromhex("00ff10"), bytes.fromhex("DE AD be ef"), bytearray.fromhex("4142"), bytes.fromhex(""))
attempt(lambda: bytes.fromhex("0g"))
attempt(lambda: bytes.fromhex("abc"))
attempt(lambda: bytes.fromhex(b"00"))
print(b"hello".find(b"l"), b"hello".find(b"z"), b"hello".find(b"l", 3), b"hello".find(b"l", 0, 2), b"hello".find(108),
      b"hello".rfind(b"l"), b"hello".index(b"lo"), b"hello".rindex(b"l"), b"hello".find(b""), b"hello".find(b"l", -2))
attempt(lambda: b"hello".index(b"z"))
print(b"banana".count(b"a"), b"banana".count(b"an"), b"banana".count(b"x"), b"banana".count(97), b"aaa".count(b"aa"),
      b"banana".count(b"a", 2), b"abc".count(b""))
print(b"hello".startswith(b"he"), b"hello".startswith(b"lo"), b"hello".endswith(b"lo"), b"hello".endswith((b"x", b"llo")),
      b"hello".startswith((b"a", b"b")), b"hello".startswith(b""), b"hello".startswith(b"ll", 2), b"hello".endswith(b"hel", 0, 3))
print(b"a,b,,c".split(b","), b"a b  c\n".split(), b"a,b,c".split(b",", 1), b"  a b c ".split(None, 1), b"".split(),
      b"abc".split(b"x"), b"a--b--c".split(b"--"), bytearray(b"a b").split())
print(b"a,b,c".rsplit(b",", 1), b"a b c".rsplit(None, 1), b"a,b".rsplit(b","), b"a\nb\r\nc\n".splitlines())
attempt(lambda: b"abc".split(b""))
print(b", ".join([b"a", b"b", b"c"]), b"".join([b"x", bytearray(b"y")]), b"-".join([]), b"-".join((b"solo",)),
      bytearray(b"+").join([b"1", b"2"]), b"".join(bytes([i]) for i in range(65, 70)))
print(b"hello".replace(b"l", b"L"), b"hello".replace(b"l", b"L", 1), b"hello".replace(b"z", b"q"), b"aaa".replace(b"a", b""),
      b"ab".replace(b"", b"-"), b"hello".replace(b"ll", b"\x00"))
print(b"  pad \n".strip(), b"  pad ".lstrip(), b"  pad ".rstrip(), b"xxhixx".strip(b"x"), b"abcba".strip(b"ab"),
      b"abc".lstrip(b"a"), b"abc".rstrip(b"c"), b"".strip(), b"\t\n ".strip())
print(b"Hello World".upper(), b"Hello World".lower(), b"Hello".swapcase(), b"hello world".capitalize(), b"\xe9A".lower())
print(b"123".isdigit(), b"12a".isdigit(), b"".isdigit(), b"abc".isalpha(), b"ab1".isalpha(), b"ab1".isalnum(),
      b" \t".isspace(), b"ABC".isupper(), b"abc".islower(), b"aBc".islower(), b"123".isupper(), b"abc".isascii(), b"\xff".isascii())
print(b"x=1".partition(b"="), b"none".partition(b"="), b"a.b.c".rpartition(b"."), b"none".rpartition(b"."))
print(b"prefix-body".removeprefix(b"prefix-"), b"body.txt".removesuffix(b".txt"), b"abc".removeprefix(b"x"))
print(b"42".zfill(5), b"-42".zfill(5), b"ab".ljust(5, b"."), b"ab".rjust(5), b"ab".center(6, b"*"), b"abcdef".zfill(3))
print(type(b"abc".upper()), type(bytearray(b"abc").upper()), type(bytearray(b"a b").split()[0]), type(b"abc".decode()))
m = b"abc".upper
print(m(), bytes.upper(b"xyz"), bytes.decode(b"abc"), bytes.hex(b"\x01"), str.encode("abc"))
attempt(lambda: b"abc".append(1))
attempt(lambda: b"abc".nosuch())
attempt(lambda: b"abc".format(1))
attempt(lambda: bytearray(b"abc").nosuch)

# ---- bytearray changes ----
ba = bytearray(b"abc")
ba.append(100)
ba.extend(b"ef")
ba.extend([103, 104])
ba.extend(bytearray(b"i"))
print(ba, len(ba))
ba[0] = 65
ba[-1] = 73
print(ba)
print(ba.pop(), ba.pop(0), ba, ba.pop(1), ba)
ba[1:3] = b"XYZ"
print(ba)
ba[:2] = b""
print(ba)
ba[0:0] = [1, 2]
print(ba)
ba[::2] = b"...."
print(ba)
del ba[0]
print(ba)
del ba[1:3]
print(ba)
ba.insert(0, 97)
ba.insert(100, 122)
ba.insert(-1, 121)
print(ba)
ba.remove(46)
ba.reverse()
print(ba)
ba += b"!!"
ba *= 2
print(ba)
alias = ba
alias.clear()
print(ba, len(ba), ba == b"", bytearray(b"abc").copy())
other = bytearray(b"same")
same = other
same += b"more"
print(other, other is same)
frozen = b"abc"
kept = frozen
kept += b"def"
print(frozen, kept)
ba = bytearray(b"0123456789")
del ba[::3]
print(ba)
ba[1::2] = b"abc"
print(ba)
attempt(lambda: bytearray(b"abc").append(256))
attempt(lambda: bytearray(b"abc").append("d"))
attempt(lambda: bytearray(b"abc").extend("def"))
attempt(lambda: bytearray(b"abc").extend([1, 300]))
attempt(lambda: bytearray().pop())
attempt(lambda: bytearray(b"abc").pop(5))
attempt(lambda: bytearray(b"abc").remove(120))


def assign(target, index, value):
    try:
        target[index] = value
        print(target)
    except Exception as e:
        print(type(e).__name__ + ":", e)


assign(b"abc", 0, 65)
assign(bytearray(b"abc"), 0, 256)
assign(bytearray(b"abc"), 0, "A")
assign(bytearray(b"abc"), 0, b"A")
assign(bytearray(b"abc"), 5, 65)


def assign_slice(target, lower, upper, step, value):
    try:
        target[lower:upper:step] = value
        print(target)
    except Exception as e:
        print(type(e).__name__ + ":", e)


assign_slice(bytearray(b"abc"), 0, 1, None, "A")
assign_slice(bytearray(b"abcd"), 0, 4, 2, b"xyz")
assign_slice(bytearray(b"abcd"), 0, 4, 2, b"xy")
assign_slice(bytearray(b"abcd"), 1, 3, None, [88, 89, 90])
assign_slice(b"abcd", 1, 3, None, b"xy")
try:
    del b"abc"[0]
except TypeError as e:
    print("TypeError:", e)

# ---- ord and chr ----
print(ord(b"a"), ord(b"\xff"), ord(bytearray(b"z")), chr(b"A"[0]), bytes([ord("A")]), chr(ord(b"a") + 1))
print("".join(chr(b) for b in b"hello"), bytes(ord(c) for c in "hello"), bytes(map(ord, "abc")))
attempt(lambda: ord(b"ab"))
attempt(lambda: ord(b""))
print(int(b"42"), int(b" 7 "), int(bytearray(b"-3")), int(b"ff", 16), float("1.5"))
attempt(lambda: int(b"4x"))

# ---- int.to_bytes and int.from_bytes ----
print((1024).to_bytes(2, "big"), (1024).to_bytes(2, "little"), (255).to_bytes(1, "big"), (0).to_bytes(3, "big"),
      (1).to_bytes(4, byteorder="little"), (65).to_bytes(), (258).to_bytes(length=2), (0).to_bytes(0, "big"))
print((-1).to_bytes(2, "big", signed=True), (-128).to_bytes(1, "big", signed=True), (127).to_bytes(1, "big", signed=True),
      (-2).to_bytes(4, "little", signed=True), (2 ** 62).to_bytes(8, "big"), (-1).to_bytes(10, "big", signed=True))
print(int.from_bytes(b"\x04\x00", "big"), int.from_bytes(b"\x04\x00", "little"), int.from_bytes(b"\xff", "big"),
      int.from_bytes(b"\xff", "big", signed=True), int.from_bytes(b"", "big"), int.from_bytes(b"\x00\x01"),
      int.from_bytes([1, 0], "big"), int.from_bytes(bytearray(b"\x01\x02"), byteorder="little"),
      int.from_bytes(b"\xff\xfe", "big", signed=True), int.from_bytes(b"\x7f\xff\xff\xff\xff\xff\xff\xff", "big"))
n = 123456789
print(int.from_bytes(n.to_bytes(4, "big"), "big") == n, int.from_bytes(n.to_bytes(8, "little"), "little") == n,
      int.from_bytes((-n).to_bytes(8, "big", signed=True), "big", signed=True) == -n)
attempt(lambda: (256).to_bytes(1, "big"))
attempt(lambda: (-1).to_bytes(1, "big"))
attempt(lambda: (128).to_bytes(1, "big", signed=True))
attempt(lambda: (-129).to_bytes(1, "big", signed=True))
attempt(lambda: (1).to_bytes(1, "middle"))
attempt(lambda: (1).to_bytes(-1, "big"))
attempt(lambda: int.from_bytes(b"\x01", "sideways"))
attempt(lambda: int.from_bytes("ab", "big"))

# ---- files of bytes ----
path = "bytes_test.bin"
with open(path, "wb") as f:
    print(f.write(b"\x00\x01\x02binary\n"), f.write(bytearray(b"second line\n")), f.write(b"\xff\xfe"))
    f.writelines([b"!", b"?"])
with open(path, "rb") as f:
    whole = f.read()
print(whole, len(whole), type(whole))
with open(path, "rb") as f:
    print(f.read(3), f.read(6), f.readline(), f.read(0), f.readline(), f.read(), f.read(), f.readline())
with open(path, "rb") as f:
    print(f.readlines())
with open(path, "rb") as f:
    for line in f:
        print("line", line)
with open(path, "ab") as f:
    f.write(b"\nappended")
print(open(path, "rb").read()[-9:])
with open(path, "wb") as f:
    f.write("text → bytes".encode("utf-8"))
with open(path) as f:
    print(f.read())
with open(path, "rb") as f:
    print(f.read().decode("utf-8"))
with open(path, "wb") as f:
    try:
        f.write("text")
    except TypeError as e:
        print("TypeError:", e)
with open(path, "w") as f:
    try:
        f.write(b"bytes")
    except TypeError as e:
        print("TypeError:", e)
attempt(lambda: open("no_such_file.bin", "rb"))
os.remove(path)
print(os.path.exists(path))

# ---- in other places ----
print(f"{b'abc'} and {b'abc'!r} and {bytearray(b'x')}", "%s %r" % (b"a", b"b"), "{}".format(b"c"))
print(b"abc" != None, b"a" if True else b"b", [b"x"] * 2, b"abc"[0] + b"abc"[1], b"abc"[0:1] + b"abc"[1:2])
print(any(b"\x00\x00"), any(b"\x00\x01"), all(b"\x01\x02"), all(b""), list(zip(b"ab", "ab")), list(map(hex, b"\x0a\xff")))
print(dict(zip([b"a", b"b"], b"AB")), {bytes([b]): b for b in b"xy"}, set(b"aabb") == {97, 98}, b"abc"[::-1][0])


def checksum(data):
    total = 0
    for byte in data:
        total = (total * 31 + byte) % 65521
    return total


print(checksum(b"hello world"), checksum(bytearray(range(256))), checksum("héllo".encode()))
packet = bytearray()
packet += (len(b"payload")).to_bytes(2, "big")
packet += b"payload"
packet.append(checksum(packet) % 256)
print(packet, packet.hex(), int.from_bytes(packet[:2], "big"), bytes(packet[2:-1]).decode())
