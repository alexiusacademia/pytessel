# re: regular expressions.
#
# Author: Alexius Academia
# Date: 2026-10-08
#
# The engine is PyTessel's own (regex.tsl), reached through the built-in
# module _re: compile() gives a pattern's number, match() one match and
# scan() every match of a text, each as a list of where the groups start
# and end. Pattern and Match are made on those here.
import _re

A = ASCII = 256
I = IGNORECASE = 2
L = LOCALE = 4
M = MULTILINE = 8
S = DOTALL = 16
U = UNICODE = 32
X = VERBOSE = 64

_FLAG_NAMES = [(256, "re.ASCII"), (2, "re.IGNORECASE"), (4, "re.LOCALE"), (8, "re.MULTILINE"),
               (16, "re.DOTALL"), (64, "re.VERBOSE")]


class error(Exception):
    """A pattern that isn't a valid regular expression."""

    __module__ = "re"

    def __init__(self, msg, pattern=None, pos=None):
        self.msg = msg
        self.pattern = pattern
        self.pos = pos
        self.lineno = None
        self.colno = None
        if pattern is not None and pos is not None:
            msg = "%s at position %d" % (msg, pos)
            before = pattern[:pos]
            self.lineno = before.count("\n") + 1
            self.colno = pos - before.rfind("\n")
            if "\n" in pattern:
                msg = "%s (line %d, column %d)" % (msg, self.lineno, self.colno)
        super().__init__(msg)


def _is_text(value):
    return isinstance(value, str)


class Match:
    """One match of a pattern in a text."""

    __module__ = "re"

    def __init__(self, pattern, string, pos, endpos, spans):
        self.re = pattern
        self.string = string
        self.pos = pos
        self.endpos = endpos
        self._spans = spans
        last = spans[len(spans) - 1]
        self.lastindex = last if last > 0 else None
        self.lastgroup = pattern._names.get(last)

    def _index(self, group):
        if isinstance(group, int):
            if 0 <= group <= self.re.groups:
                return group
        elif isinstance(group, str):
            if group in self.re.groupindex:
                return self.re.groupindex[group]
        raise IndexError("no such group")

    def _text(self, index, default=None):
        start = self._spans[2 * index]
        if start < 0:
            return default
        return _re.text(self.string, start, self._spans[2 * index + 1])

    def group(self, *groups):
        if len(groups) == 0:
            return self._text(0)
        if len(groups) == 1:
            return self._text(self._index(groups[0]))
        return tuple([self._text(self._index(g)) for g in groups])

    def __getitem__(self, group):
        return self._text(self._index(group))

    def groups(self, default=None):
        return tuple([self._text(i, default) for i in range(1, self.re.groups + 1)])

    def groupdict(self, default=None):
        out = {}
        for name in self.re.groupindex:
            out[name] = self._text(self.re.groupindex[name], default)
        return out

    def start(self, group=0):
        return self._spans[2 * self._index(group)]

    def end(self, group=0):
        return self._spans[2 * self._index(group) + 1]

    def span(self, group=0):
        index = self._index(group)
        return (self._spans[2 * index], self._spans[2 * index + 1])

    def expand(self, template):
        return _expand(_template(self.re, template), self.string, self._spans)

    def __bool__(self):
        return True

    def __repr__(self):
        return "<re.Match object; span=%r, match=%r>" % (self.span(), self.group())


class Pattern:
    """A compiled regular expression."""

    __module__ = "re"

    def __init__(self, pattern, flags, code, groups, groupindex):
        self.pattern = pattern
        self.flags = flags
        self.groups = groups
        self.groupindex = groupindex
        self._code = code
        self._names = {}
        for name in groupindex:
            self._names[groupindex[name]] = name

    def __repr__(self):
        text = repr(self.pattern)
        if len(text) > 200:
            text = text[:200]
        names = [name for bit, name in _FLAG_NAMES if self.flags & bit]
        if names:
            return "re.compile(%s, %s)" % (text, "|".join(names))
        return "re.compile(%s)" % text

    def __eq__(self, other):
        return isinstance(other, Pattern) and self.pattern == other.pattern and self.flags == other.flags

    def __hash__(self):
        return hash((self.pattern, self.flags))

    def _range(self, string, pos, endpos):
        if not _is_text(string):
            raise TypeError("expected string or bytes-like object")
        size = len(string)
        if endpos is None or endpos > size:
            endpos = size
        if endpos < 0:
            endpos = 0
        if pos < 0:
            pos = 0
        if pos > size:
            pos = size
        return pos, endpos

    def _one(self, string, pos, endpos, mode):
        pos, endpos = self._range(string, pos, endpos)
        spans = _re.match(self._code, string, pos, endpos, mode)
        if spans is None:
            return None
        return Match(self, string, pos, endpos, spans)

    def match(self, string, pos=0, endpos=None):
        return self._one(string, pos, endpos, 0)

    def fullmatch(self, string, pos=0, endpos=None):
        return self._one(string, pos, endpos, 1)

    def search(self, string, pos=0, endpos=None):
        return self._one(string, pos, endpos, 2)

    def finditer(self, string, pos=0, endpos=None):
        pos, endpos = self._range(string, pos, endpos)
        found = _re.scan(self._code, string, pos, endpos, 0)
        return iter([Match(self, string, pos, endpos, spans) for spans in found])

    def findall(self, string, pos=0, endpos=None):
        pos, endpos = self._range(string, pos, endpos)
        groups = self.groups
        # Where every wanted part starts and ends, then all of them at once.
        bounds = []
        for spans in _re.scan(self._code, string, pos, endpos, 0):
            if groups == 0:
                bounds.append(spans[0])
                bounds.append(spans[1])
            else:
                for i in range(2, 2 * groups + 2):
                    bounds.append(spans[i])
        parts = _re.cut(string, bounds)
        if groups <= 1:
            return [part if part is not None else "" for part in parts]
        out = []
        for i in range(0, len(parts), groups):
            out.append(tuple([part if part is not None else "" for part in parts[i:i + groups]]))
        return out

    def split(self, string, maxsplit=0):
        pos, endpos = self._range(string, 0, None)
        if maxsplit < 0:
            return [string]
        bounds = []
        last = 0
        for spans in _re.scan(self._code, string, 0, endpos, maxsplit):
            bounds.append(last)
            bounds.append(spans[0])
            for i in range(2, 2 * self.groups + 2):
                bounds.append(spans[i])
            last = spans[1]
        bounds.append(last)
        bounds.append(endpos)
        return _re.cut(string, bounds)

    def subn(self, repl, string, count=0):
        pos, endpos = self._range(string, 0, None)
        function = None
        parts = None
        if callable(repl):
            function = repl
        else:
            if not _is_text(repl):
                raise TypeError("expected str instance, %s found" % type(repl).__name__)
            parts = _template(self, repl)
            if len(parts) == 1 and _is_text(parts[0]):
                # (Nothing of the match in it: the same text each time.)
                repl = parts[0]
                parts = None
            elif len(parts) == 0:
                repl = ""
                parts = None
        if count < 0:
            return string, 0
        found = _re.scan(self._code, string, 0, endpos, count)
        # What's between the matches, all at once.
        bounds = []
        last = 0
        for spans in found:
            bounds.append(last)
            bounds.append(spans[0])
            last = spans[1]
        bounds.append(last)
        bounds.append(endpos)
        between = _re.cut(string, bounds)
        pieces = []
        done = 0
        for spans in found:
            pieces.append(between[done])
            if function is not None:
                pieces.append(function(Match(self, string, 0, endpos, spans)))
            elif parts is not None:
                pieces.append(_expand(parts, string, spans))
            else:
                pieces.append(repl)
            done += 1
        pieces.append(between[done])
        return "".join(pieces), done

    def sub(self, repl, string, count=0):
        return self.subn(repl, string, count)[0]


# ---- what replaces a match: "\1-\g<name>" ----

_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "f": "\f", "v": "\v", "a": "\a", "b": "\b", "\\": "\\"}
_ASCII_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_DIGITS = "0123456789"
_OCTAL = "01234567"


def _template(pattern, repl):
    """A replacement text as a list of its parts: texts, and groups' numbers."""
    if "\\" not in repl:
        return [repl] if repl else []
    parts = []
    text = []
    size = len(repl)
    i = 0
    while i < size:
        c = repl[i]
        if c != "\\":
            text.append(c)
            i += 1
            continue
        at = i
        i += 1
        if i >= size:
            raise error("bad escape (end of pattern)", repl, at)
        c = repl[i]
        i += 1
        group = -1
        if c == "g":
            if i >= size or repl[i] != "<":
                raise error("missing <", repl, i)
            i += 1
            start = i
            end = repl.find(">", i)
            if end < 0:
                if i >= size:
                    raise error("missing group name", repl, start)
                raise error("missing >, unterminated name", repl, start)
            name = repl[i:end]
            i = end + 1
            if name == "":
                raise error("missing group name", repl, start)
            if name.isdigit():
                group = int(name)
                if group > pattern.groups:
                    raise error("invalid group reference %d" % group, repl, start)
            else:
                if not name.isidentifier():
                    raise error("bad character in group name %r" % name, repl, start)
                if name not in pattern.groupindex:
                    raise IndexError("unknown group name %r" % name)
                group = pattern.groupindex[name]
        elif c == "0":
            # \0, \012: a character by its number in base 8.
            value = 0
            used = 0
            while used < 2 and i < size and repl[i] in _OCTAL:
                value = value * 8 + int(repl[i])
                i += 1
                used += 1
            text.append(chr(value))
        elif c in _DIGITS:
            group = int(c)
            if i < size and repl[i] in _DIGITS:
                if c in _OCTAL and repl[i] in _OCTAL and i + 1 < size and repl[i + 1] in _OCTAL:
                    value = int(c) * 64 + int(repl[i]) * 8 + int(repl[i + 1])
                    i += 2
                    if value > 255:
                        raise error("octal escape value %s outside of range 0-0o377" % repl[at:i], repl, at)
                    text.append(chr(value))
                    group = -1
                else:
                    group = group * 10 + int(repl[i])
                    i += 1
            if group > pattern.groups:
                raise error("invalid group reference %d" % group, repl, at + 1)
        elif c in _ESCAPES:
            text.append(_ESCAPES[c])
        elif c in _ASCII_LETTERS:
            raise error("bad escape \\%s" % c, repl, at)
        else:
            text.append("\\" + c)
        if group >= 0:
            if text:
                parts.append("".join(text))
                text = []
            parts.append(group)
    if text:
        parts.append("".join(text))
    return parts


def _expand(parts, string, spans):
    out = []
    for part in parts:
        if isinstance(part, int):
            start = spans[2 * part]
            if start >= 0:
                out.append(_re.text(string, start, spans[2 * part + 1]))
        else:
            out.append(part)
    return "".join(out)


# ---- the module's functions ----

_cache = {}


def compile(pattern, flags=0):
    if isinstance(pattern, Pattern):
        if flags:
            raise ValueError("cannot process flags argument with a compiled pattern")
        return pattern
    if not _is_text(pattern):
        raise TypeError("first argument must be string or compiled pattern")
    key = (pattern, flags)
    if key in _cache:
        return _cache[key]
    made = _re.compile(pattern, flags)
    if len(made) == 2:
        if made[1] < 0:
            raise error(made[0])
        raise error(made[0], pattern, made[1])
    code, groups, names, numbers, flags = made
    if not flags & 256:
        flags = flags | 32
    groupindex = {}
    for i in range(len(names)):
        groupindex[names[i]] = numbers[i]
    compiled = Pattern(pattern, flags, code, groups, groupindex)
    if len(_cache) >= 512:
        _cache.clear()
    _cache[key] = compiled
    return compiled


def purge():
    _cache.clear()


def match(pattern, string, flags=0):
    return compile(pattern, flags).match(string)


def fullmatch(pattern, string, flags=0):
    return compile(pattern, flags).fullmatch(string)


def search(pattern, string, flags=0):
    return compile(pattern, flags).search(string)


def sub(pattern, repl, string, count=0, flags=0):
    return compile(pattern, flags).sub(repl, string, count)


def subn(pattern, repl, string, count=0, flags=0):
    return compile(pattern, flags).subn(repl, string, count)


def split(pattern, string, maxsplit=0, flags=0):
    return compile(pattern, flags).split(string, maxsplit)


def findall(pattern, string, flags=0):
    return compile(pattern, flags).findall(string)


def finditer(pattern, string, flags=0):
    return compile(pattern, flags).finditer(string)


_SPECIAL = "()[]{}?*+-|^$\\.&~# \t\n\r\v\f"


def escape(pattern):
    """The text as a pattern that matches exactly it."""
    out = []
    for c in pattern:
        if c in _SPECIAL:
            out.append("\\" + c)
        else:
            out.append(c)
    return "".join(out)
