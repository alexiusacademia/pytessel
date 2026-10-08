# The re module: regular expressions.
#
# Author: Alexius Academia
# Date: 2026-10-08
import re


def show(pattern, text, flags=0):
    m = re.search(pattern, text, flags)
    if m is None:
        print(repr(pattern), repr(text), "-> no match")
    else:
        print(repr(pattern), repr(text), "->", repr(m.group()), m.span(), m.groups())


# ---- the functions ----
print(re.match(r"a+", "aaab"), re.match(r"a+", "baaa"), re.search(r"a+", "baaa"))
print(re.search(r"\d+", "abc 123 def").group(), re.fullmatch(r"\d+", "123"), re.fullmatch(r"\d+", "123a"), re.fullmatch(r"\d+|\d+a", "123a").group())
print(re.findall(r"\w+", "hello, big world!"), re.findall(r"x", "abc"), re.findall(r"", "ab"))
print(re.sub(r"(\w+)@(\w+)", r"\2 at \1", "joe@example and ann@home"), re.subn(r"\s+", " ", "a  b \t c"))
print(re.split(r"[,;]\s*", "a, b;c,d"), re.split(r"\d", "a1b2c"), re.split(r"x", "abc"))
print([m.group() for m in re.finditer(r"[aeiou]", "education")], [m.start() for m in re.finditer(r"o", "foo boo")])
m = re.match(r"(?P<year>\d{4})-(?P<month>\d\d)-(\d\d)", "2024-05-17 and more")
print(m.group(), m.group(0), m.group(1), m.group("year"), m["month"], m[3], m.group(1, 3), m.group("month", 1, 0))
print(m.groups(), m.groupdict(), m.span(), m.start(), m.end(), m.span(2), m.start("month"), m.end(3), m.lastindex, m.lastgroup)
print(m.string, m.pos, m.endpos, m.re.pattern, bool(m), m.expand(r"\3/\2/\1 \g<year> \g<1>"), repr(m))
print(re.match("(a)|(b)", "b").groups(), re.match("(a)|(b)", "b").groups("-"), re.match("(a)|(b)", "b").lastindex, re.match("((a)(b))", "ab").lastindex)
print(re.match("(a)?(b)", "b").span(1), re.match("(a)?(b)", "b").start(1), re.match("(a)?b", "b").group(1), re.match("(?P<n>a)?b", "b").groupdict("none"))
print(re.match("a", "a").lastindex, re.match("a", "a").lastgroup, re.match("a", "a").groups(), re.match("a", "a").groupdict(), re.match("(a)(?P<b>b)?", "a").lastgroup)

# ---- empty matches ----
print(re.findall(r"a*", "baac"), re.split(r"x*", "axbc"), re.sub(r"x*", "-", "abxd"), re.sub(r"", "-", "abc"))
print(re.findall(r"\b", "ab cd"), re.split(r"\b", "ab cd"), re.sub(r"\B", "-", "abc de"), re.sub(r"^", ">", "a\nb", flags=re.M))
print([m.span() for m in re.finditer(r"a|", "baab")], re.findall(r"a??", "aa"), re.sub(r"a*?", "-", "aa"), re.split(r"", "abc"))
print(re.findall(r"\d*", "a12b3"), re.sub(r"\d*", "#", "a12b3"), re.split(r"(?=b)", "abab"), re.findall(r"$", "ab\n"), re.sub("$", "!", "ab\n"))

# ---- groups in findall and split ----
print(re.findall(r"(\w)(\d)?", "a1b c2"), re.findall(r"(\w)=", "a=b= c"), re.findall(r"(?:\w)=(\d)|x", "a=1x"))
print(re.split(r"(-)|(\+)", "a-b+c"), re.split(r"(\s+)", "a b  c"), re.split(r"\s+", " a b  c ", maxsplit=2), re.split(r"\s+", "a b c", 1))
print(re.findall(r"(\d+)\.(\d+)", "1.2 33.44 5"), re.findall(r"((a)(b)?)", "ab a"), re.split(r"(a)(b)?", "xabya"))

# ---- quantifiers ----
for p, s in [(r"a{2,3}", "aaaa"), (r"a{2,3}?", "aaaa"), (r"a{,2}", "aaa"), (r"a{2,}", "aaaaa"), (r"a{2}", "aaa"), (r"a{0}b", "ab"),
             (r"<.*>", "<a><b>"), (r"<.*?>", "<a><b>"), (r"a+?", "aaa"), (r"a??b", "ab"), (r"x{}", "x{}"), (r"x{a}", "x{a}"),
             (r"x{1,2", "x{1,2"), (r"(ab)*", "ababa"), (r"(a|ab)(c|bcd)(d*)", "abcd"), (r"(a*)*", "b"), (r"(a*)+", "b"),
             (r"(a|b)*?c", "abac"), (r"(?:a|b)+", "abba"), (r"(a+)+b", "aaab"), (r"(a?)*", "aa"), (r"(a?)+?b", "aab"),
             (r"(\d{1,3})(,\d{3})*", "1,234,567 x"), (r"\d{3}-\d{4}", "call 555-1234 now"), (r"(a|b){2}", "abab"),
             (r"a*?b*?c", "aabbc"), (r"(a+|b+)*c", "aabbaac"), (r"(?:(a)|(b))+", "ab"), (r".{3}", "ab\ncdef"), (r"a{3,5}?a", "aaaaaa"),
             (r"(a{1,2}){2}", "aaaa"), (r"x*", ""), (r"x+", ""), (r"(|a)+", "aa"), (r"(a|)+", "aa"), (r"\w{2,3}?\b", "abcd ef")]:
    show(p, s)

# ---- sets of characters ----
for p, s in [(r"[a-c]+", "abcd"), (r"[^a-c]+", "xyzabc"), (r"[]a]+", "]a]"), (r"[^]a]+", "xy]"), (r"[a\-z]+", "a-z"),
             (r"[\d.]+", "3.14x"), (r"[\w-]+", "ab-c d"), (r"[a-]+", "a-a"), (r"[-a]+", "a-a"), (r"[\]]+", "]]"),
             (r"[\s\S]+", "a\nb"), (r"[^\W\d_]+", "abc1"), (r"[\x41-\x43]+", "ABCD"), (r"[\n]", "\n"), (r"[.]", "."), (r"[.]", "a"),
             (r"\D+", "ab1"), (r"\S+", "ab c"), (r"\W+", ", !a"), (r"[A-Za-z_][A-Za-z0-9_]*", "9 _x9 y"), (r"[+*?.()|^$]+", "a+*?.()|^$b"),
             (r"[^\n]+", "ab\ncd"), (r"[a-zA-Z]+\d", "abc5"), (r"[\[\]]", "a[b"), (r"[a^]+", "^a^"), (r"[^^]+", "ab^"), (r"[\\]+", "a\\\\b"),
             (r"[\t ]+", "a \t b"), (r"[0-9a-fA-F]+", "xDEADbeef!"), (r"[\u00e0-\u00ff]+", "caf\u00e9"), (r"[{}]", "a{b")]:
    show(p, s)

# ---- escapes ----
for p, s in [(r"\.", "a.b"), (r"\\", "a\\b"), (r"\$\d+", "cost $15"), (r"\(\w+\)", "f(x)"), (r"a\+b", "a+b"), (r"\x41\u0042", "AB"),
             (r"\t\n", "a\t\nb"), (r"\d\D\s\S\w\W", "1a b_!"), (r"\/\-\@", "/-@"), (r"\141", "a"), (r"\101\102", "AB"),
             (r"a\ b", "a b"), (r"\#", "#"), (r"\{2\}", "{2}"), (r"\^\|", "^|")]:
    show(p, s)

# ---- anchors and flags ----
print(re.findall(r"^\w+", "ab cd\nef gh"), re.findall(r"^\w+", "ab cd\nef gh", re.M), re.findall(r"\w+$", "ab cd\nef gh"), re.findall(r"\w+$", "ab cd\nef gh", re.MULTILINE))
print(re.findall(r"\w+$", "ab cd\n"), re.search(r"\Aab", "ab").span(), re.search(r"cd\Z", "ab cd\n"), re.search(r"cd$", "ab cd\n").span(), re.search(r"\Ab", "ab"), re.findall(r"\A\w", "a\nb", re.M), re.findall(r"\w\Z", "a\nb", re.M))
print(re.findall(r"a.c", "abc a\nc"), re.findall(r"a.c", "abc a\nc", re.S), re.findall(r"a.c", "ABC a\nc", re.I | re.DOTALL))
print(re.findall(r"(?i)hello", "Hello HELLO hello"), re.findall(r"[a-c]+", "AbC", re.IGNORECASE), re.findall(r"(?i:a)b", "Ab AB ab"), re.findall(r"A(?-i:b)", "ab AB Ab", re.I))
print(re.findall(r"[^a]+", "bAb", re.I), re.findall(r"\w+", "MiXeD", re.I), re.sub("x", "-", "aXbx", flags=re.I), re.split("x", "aXb", flags=re.I), re.search("STRASSE", "strasse", re.I).span())
print(re.findall(r"""\d+  # digits
                     \s*  # spaces
                     [a-z]+ # a word""", "12 ab 3cd", re.X), re.findall(r"(?x) a b \  c [ ] \# # a comment", "ab c #"))
print(re.search(r"(?m)^b$", "a\nb\nc").span(), re.search(r"(?s)a.b", "a\nb").span(), re.search(r"(?im)^B", "a\nb").span(), re.findall(r"(?mi)^[a-z]+$", "One\ntwo 2\nTHREE"))
print(re.findall(r"\bfoo\b", "foo foobar barfoo foo."), re.findall(r"\Boo", "foo oo"), re.findall(r"\b\w", "hello big-world"), re.sub(r"\b(\w)", lambda m: m.group(1).upper(), "the quick fox"))
print(re.match(r"\u00e9+", "\u00e9\u00e9\u00e9").span(), re.findall(r"\w+", "na\u00efve caf\u00e9"), re.findall("\u00c9", "\u00e9\u00c9", re.I), re.findall(r"\w+", "na\u00efve caf\u00e9", re.A), re.findall(r"\d+", "12 34"))
print(re.compile(r"a.c", re.S | re.I | re.M).flags, re.compile("a").flags, re.compile("(?i)a").flags, re.compile("a", re.A).flags, re.compile("(?x) a", re.M).flags)
print(re.I == re.IGNORECASE, re.M == re.MULTILINE, re.S == re.DOTALL, re.X == re.VERBOSE, re.A == re.ASCII, int(re.I | re.M))

# ---- back references, lookahead, lookbehind ----
print(re.search(r"(\w)\1", "hello").group(), re.search(r"(?P<q>['\"]).*?(?P=q)", "say 'hi' now").group(), re.findall(r"\b(\w+) \1\b", "the the cat sat sat"))
print(re.search(r"(a)(b)\2\1", "abba").span(), re.match(r"(a)?\1", "b"), re.search(r"(?i)(a)\1", "aA").group(), re.sub(r"(\w)\1+", r"\1", "aaabbbcd"))
print(re.findall(r"\w+(?=,)", "a, b, c"), re.findall(r"\w+(?!,)\b", "ab, cd, ef"), re.findall(r"q(?=u)", "quit qat"), re.findall(r"q(?!u)", "quit qat"))
print(re.findall(r"(?<=\$)\d+", "$10 20 $30"), re.findall(r"(?<!\$)\b\d+", "$10 20 $30"), re.sub(r"(?<=a)b", "X", "ab cb ab"), re.findall(r"(?<=^)\w|(?<=,)\w", "a,b,c"))
print(re.match(r"(?=(a+))a*b", "aaab").groups(), re.match(r"(?!x)(\w)", "ab").group(1), re.search(r"(?<=(a))b", "ab").groups(), re.findall(r"(?<=ab|cd)e", "abe cde xe"))
print(re.sub(r"(?<=\d)(?=(\d{3})+$)", ",", "1234567"), re.findall(r"\b(?!the\b)\w+", "the cat the dog"), re.search(r"(?<!\w)un\w+", "run undo").group(), re.findall(r"(?<=[a-z])(?=[A-Z])", "camelCaseText"))
print(re.split(r"(?<=[.!?])\s+", "One. Two! Three? Four"), re.sub(r"(?<![a-z])cat(?![a-z])", "dog", "cat concat cats cat."), re.match(r"(?:(?=a)a|b)+", "abab").group())
print(re.findall(r"(?<=\bMr\. )\w+", "Mr. Smith and Mr. Jones"), re.search(r"(?<=a)(?<!b)c", "ac"), re.search(r"a(?=b(?=c))", "abc").span(), re.search(r"(?<!(?<=a)b)c", "abc"), re.search(r"(?<!(?<=a)b)c", "xbc").span())

# ---- replacements ----
print(re.sub(r"(\d+)", r"<\g<1>>", "a1b22"), re.sub(r"(?P<n>\d)", r"\g<n>\g<n>", "a1"), re.sub("a", r"\\n\n\t", "a") == "\\n\n\t", re.sub("(a)", r"\g<1>0", "a"))
print(re.sub(r"(a)|(b)", r"[\1\2]", "ab"), re.subn("a", "b", "aaa", count=2), re.sub("a", "b", "aaa", 1), re.sub("a", "", "banana"), re.sub("x", "y", ""), re.subn("x", "y", "abc"))
print(re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "a1 b22 c333"), re.sub(r"(\w+) (\w+)", lambda m: m.group(2) + " " + m.group(1), "hello world"))
print(re.sub(r"(?P<first>\w+) (?P<second>\w+)", r"\g<second> \g<first>", "hello world"), re.sub(r"\s+", " ", "  many   spaces\there "), re.sub(r"[aeiou]", "*", "education", count=3))
print(re.sub(r"(.)(.)", r"\2\1", "abcdef"), re.sub("a|b", lambda m: {"a": "1", "b": "2"}[m.group()], "abc"), re.sub(r"\\", "/", "a\\b\\c"), re.sub(r"/", r"\\", "a/b"), re.sub("b", r"\x", "abc") if False else "skip")
print(re.sub(r"(a)(b)?", r"\1[\2]", "ac ab"), re.sub("a", "&", "aa"), re.sub("a", r"\g<0>\g<0>", "ab"), re.sub("(?P<x>a)", r"\1\g<x>", "a"), re.sub("a", r"\07", "a") == "\x07", re.sub("(a)", r"\1\101", "a"))
counter = [0]


def numbered(match):
    counter[0] += 1
    return "%s%d" % (match.group(), counter[0])


print(re.sub(r"[a-z]", numbered, "abc"), counter, re.sub("a", lambda m: "", "banana"), re.sub("(?i)A", lambda m: m.group().swapcase(), "aAbB"))
template = "Dear {name}, your order {id} ships {when}."
print(re.sub(r"\{(\w+)\}", lambda m: {"name": "Ann", "id": "#42"}.get(m.group(1), "?"), template))

# ---- errors ----
for p in [r"(", r")", r"a**", r"*a", r"[a", r"\q", r"(?P<a>x)(?P<a>y)", r"(?P=x)", r"\1", r"(a)\2", r"[z-a]", r"a{3,1}", r"(?<=a+)b",
          r"(?z)", r"(?P<1a>x)", r"(?P<a", r"(?", r"x(?#c", "a\\", r"(?P<a>x)(?P=a", r"(a\1)", r"+", r"a|*", r"(?Px)", r"(?<x)",
          r"[\d-a]", "a\n(", r"{1}", r"a{1}{2}", r"^*", r"$?", r"\x4", r"[a-\d]", r"a)b", r"((a)", r"[]", r"a++", r"(?P<>x)", r"\8", r"(?<!a*)b",
          r"a{2}*", r"(?:", r"[b-a]", r"\N", r"a?*", r"(?P<n>a)(?P=m)", r"abc\\", r"\\"]:
    try:
        re.compile(p)
        print(repr(p), "ok")
    except re.error as e:
        print(repr(p), "error:", e, "|", e.msg, e.pos, e.lineno, e.colno, e.pattern == p)
for attempt in [lambda: re.sub("a", r"\2", "a"), lambda: re.sub("(a)", r"\g<1", "a"), lambda: re.sub("(a)", r"\q", "a"), lambda: re.sub("(a)", r"\g", "a"),
                lambda: re.sub("(a)", r"\g<>", "a"), lambda: re.sub("(a)", r"\g<2>", "a"), lambda: re.sub("(a)", "\\", "a"), lambda: re.sub("(a)", r"\g<a-b>", "a")]:
    try:
        print(attempt())
    except re.error as e:
        print("error:", e)
m = re.match(r"(a)(?P<b>b)", "ab")
for attempt in [lambda: m.group(3), lambda: m.group("zz"), lambda: m.start(5), lambda: m[9], lambda: m.span("c"), lambda: m.group(-1), lambda: re.sub("(a)", r"\g<x>", "a")]:
    try:
        print(attempt())
    except IndexError as e:
        print("IndexError:", e)
for attempt in [lambda: re.match(1, "a"), lambda: re.match("a", 1), lambda: re.compile(None), lambda: re.findall("a", None), lambda: re.sub("a", 5, "a")]:
    try:
        print(attempt())
    except TypeError as e:
        print("TypeError")
try:
    re.compile(re.compile("a"), re.I)
except ValueError as e:
    print("ValueError:", e)
print(issubclass(re.error, Exception), re.compile(re.compile("a")).pattern)

# ---- Pattern objects ----
p = re.compile(r"(\d+)-(?P<b>\d+)", re.I)
print(p.pattern, p.flags, p.groups, p.groupindex, p, re.compile("a"), re.compile("a", re.M | re.S), re.compile(r"\d+\s", re.X))
print(p.match("12-34").group(1, 2), p.search("x 1-2", 1).span(), p.match("x1-2", 1).group(0), p.search("1-2", 0, 2), p.match("1-23", 0, 3).group())
print(p.findall("1-2 3-4", 2), p.sub("#", "1-2 3-4"), p.split("a1-2b"), p.fullmatch("1-2").span(), p.subn("#", "1-2 3-4"), p.fullmatch("x1-2y", 1, 4).span())
print([m.group("b") for m in p.finditer("1-2 30-40")], [m.span() for m in p.finditer("1-2 30-40", 2)], p.sub(r"\2-\1", "1-2"), p.sub(lambda m: m["b"], "1-2", 1), p.split("1-2x3-4y", 1))
m = p.match("12-34")
print(m.re is p, m.re.groups, p.search("zz", 5), p.match("12-34", 10), p.match("12-34", -5).span(), p.match("12-34", 0, 100).span(), p.search("a 1-2", endpos=3))
word = re.compile(r"\w+")
print(word.findall("one two  three"), word.search("  hi").start(), word.match("  hi"), word.match("  hi", 2).group(), word.fullmatch("hi there"), len(word.findall("a " * 50)))
print(re.compile("a") == re.compile("a"), re.compile("a") == re.compile("a", re.I), re.compile("a") is re.compile("a"), {re.compile("x"): 1}[re.compile("x")])
print(re.escape("a.b*c [d] 100%"), re.escape("https://x.y/z?q=1&r=2"), re.escape(""), re.escape("plain_text-1"), re.match(re.escape("1+1=2?"), "1+1=2?").group())
print(re.fullmatch(re.escape("[a](b){c}^$|\\"), "[a](b){c}^$|\\") is not None, re.split(re.escape("."), "a.b.c"), re.purge())

# ---- things people do with it ----
text = "The quick brown fox jumps over the lazy dog. " * 40
print(len(re.findall(r"\b\w{5}\b", text)), len(re.findall(r"o", text)), re.sub(r"\s+", " ", text)[:20], len(re.split(r"\.\s*", text)), len(re.findall(r"(?i)the", text)))
tokens = re.compile(r"\s*(?:(\d+\.?\d*)|(\w+)|(.))")
print([m.lastindex for m in tokens.finditer("x = 3.5 * (y + 12)")], [m.group(m.lastindex) for m in tokens.finditer("x = 3.5 * (y + 12)")])


def tokenize(source):
    spec = [("NUMBER", r"\d+(?:\.\d+)?"), ("NAME", r"[A-Za-z_]\w*"), ("OP", r"[-+*/()=]"), ("SKIP", r"\s+"), ("BAD", r".")]
    scanner = re.compile("|".join("(?P<%s>%s)" % pair for pair in spec))
    out = []
    pos = 0
    while pos < len(source):
        m = scanner.match(source, pos)
        if m.lastgroup != "SKIP":
            out.append((m.lastgroup, m.group()))
        pos = m.end()
    return out


print(tokenize("rate = (base + 2.5) * 10 ?"))
log = "2024-01-02 ERROR disk full\n2024-01-03 INFO ok\n2024-01-04 ERROR net down"
print(re.findall(r"^(\S+) ERROR (.*)$", log, re.M), [m.groupdict() for m in re.finditer(r"(?P<date>\S+) (?P<level>[A-Z]+)", log)][1])
print(re.match(r"^(\w+)\s*=\s*(.*?)\s*$", "key =  some value  ").groups(), re.match(r"\s*(\w+)\s*:\s*(\d+)\s*$", "  port : 8080 ").groups())
email = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
print([bool(email.match(x)) for x in ["a@b.co", "bad@", "x.y+z@d-e.org", "@no.pe", "two@@x.y"]])
print(re.findall(r"(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)", "ip 192.168.1.254 and 10.0.0.1 not 999.1"))
print(re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}\b", "#fff #12AB9f #12 #abcd"), re.findall(r"<(\w+)[^>]*>", "<a href='x'><b><br/>"), re.sub(r"<[^>]+>", "", "<p>Hi <b>there</b></p>"))
print(re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", "x=3 y=-2.5 z=1e10 w=.5e-3"), re.findall(r"\b[A-Z][a-z]+\b", "Alice met Bob in Paris, not LONDON"))
print(re.sub(r"(?<!^)(?=[A-Z])", "_", "camelCaseName").lower(), re.sub(r"_([a-z])", lambda m: m.group(1).upper(), "snake_case_name"), re.sub(r"(\d)(?=(\d{3})+(?!\d))", r"\1,", "1234567.891"))
print(re.split(r"\s*[,;]\s*|\s+", "a, b;c  d"), dict(re.findall(r"(\w+)=(\w+)", "a=1&b=two&c=3")), re.fullmatch(r"\d{4}-\d{2}-\d{2}", "2024-05-17") is not None)
print(re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', r'say "hi \"there\"" and "bye"'), re.match(r"(\w+)://([^/:]+)(?::(\d+))?(/.*)?", "https://example.com:8080/a/b?c=d").groups())
print(re.sub(r"^\s+|\s+$", "", "  trim me  "), re.sub(r"(?m)^", "> ", "line one\nline two"), re.sub(r"(?m)\s+$", "", "a  \nb\t\n"), re.findall(r"(?s)/\*.*?\*/", "a /* one */ b /* two\nlines */"))
print(re.match(r"(\d+)\s*(kb|mb|gb)?$", "512 MB", re.I).groups(), re.search(r"(?P<h>\d{1,2}):(?P<m>\d{2})(?::(?P<s>\d{2}))?", "at 9:05 today").groupdict())
words = re.findall(r"[a-z']+", "It's the end of the world as we know it, and I feel fine.".lower())
print(words, len(words), sorted(set(w for w in words if re.fullmatch(r"\w{3}", w))))
print(re.search(r"(a+)+$", "a" * 18 + "b"), re.match(r"(x+x+)+y", "x" * 14), re.search(r"^(\w+\s?)*$", "one two three four five six!"))
long_text = "ab" * 5000
print(len(re.findall(r"ab", long_text)), re.match(r"(?:ab)*", long_text).end(), re.match(r".*", long_text + "\nx").end(), re.search(r"b{2}", long_text), len(re.sub("a", "", long_text)), len(re.split("b", long_text)))
print(re.match(r"\d+", "1" * 3000).end(), re.fullmatch(r"(?:a|b)*", "ab" * 2000).end(), re.search(r"x", "y" * 20000), re.search(r".*?z", "y" * 5000 + "z").end())
