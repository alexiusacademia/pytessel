# textwrap: wrapping and filling paragraphs of text.
#
# Author: Alexius Academia
# Date: 2026-10-08
#
# After CPython's textwrap: the text is cut into chunks (words, runs of
# spaces, the parts of hyphenated words) with a regular expression, and
# the chunks are put on lines.
import re

_whitespace = "\t\n\x0b\x0c\r "


def _expandtabs(text, tabsize):
    # str.expandtabs: each tab becomes spaces up to the next tab stop.
    if "\t" not in text:
        return text
    out = []
    column = 0
    for c in text:
        if c == "\t":
            if tabsize > 0:
                n = tabsize - column % tabsize
                out.append(" " * n)
                column += n
        elif c == "\n" or c == "\r":
            out.append(c)
            column = 0
        else:
            out.append(c)
            column += 1
    return "".join(out)


def _spaces_only(text):
    # Every kind of white space becomes a plain space.
    out = []
    changed = False
    for c in text:
        if c in "\t\n\x0b\x0c\r":
            out.append(" ")
            changed = True
        else:
            out.append(c)
    return "".join(out) if changed else text


def _lines_with_ends(text):
    # str.splitlines(keepends=True).
    lines = []
    start = 0
    i = 0
    size = len(text)
    while i < size:
        c = text[i]
        if c == "\r" and i + 1 < size and text[i + 1] == "\n":
            i += 2
            lines.append(text[start:i])
            start = i
        elif c in "\n\r\x0b\x0c\x1c\x1d\x1e\x85  ":
            i += 1
            lines.append(text[start:i])
            start = i
        else:
            i += 1
    if start < size:
        lines.append(text[start:])
    return lines


_word_punct = "[\\w!\"'&.,?]"
_letter = "[^\\d\\W]"
_ws = "[" + re.escape(_whitespace) + "]"
_nws = "[^" + _ws[1:]

_wordsep_re = re.compile((r"""
    ( # any whitespace
      WS+
    | # em-dash between words
      (?<=WP) -{2,} (?=\w)
    | # word, possibly hyphenated
      NWS+? (?:
        # hyphenated word
          -(?: (?<=LT{2}-) | (?<=LT-LT-))
          (?= LT -? LT)
        | # end of word
          (?=WS|\Z)
        | # em-dash
          (?<=WP) (?=-{2,}\w)
        )
    )""").replace("NWS", _nws).replace("WS", _ws).replace("WP", _word_punct).replace("LT", _letter), re.VERBOSE)

_wordsep_simple_re = re.compile("(" + _ws + "+)")

_sentence_end_re = re.compile(r"[a-z][\.\!\?][\"\']?\Z")


class TextWrapper:
    """Wraps text: wrap() gives the lines, fill() the lines as one text."""

    def __init__(self, width=70, initial_indent="", subsequent_indent="", expand_tabs=True,
                 replace_whitespace=True, fix_sentence_endings=False, break_long_words=True,
                 drop_whitespace=True, break_on_hyphens=True, tabsize=8, max_lines=None,
                 placeholder=" [...]"):
        self.width = width
        self.initial_indent = initial_indent
        self.subsequent_indent = subsequent_indent
        self.expand_tabs = expand_tabs
        self.replace_whitespace = replace_whitespace
        self.fix_sentence_endings = fix_sentence_endings
        self.break_long_words = break_long_words
        self.drop_whitespace = drop_whitespace
        self.break_on_hyphens = break_on_hyphens
        self.tabsize = tabsize
        self.max_lines = max_lines
        self.placeholder = placeholder

    def _munge_whitespace(self, text):
        if self.expand_tabs:
            text = _expandtabs(text, self.tabsize)
        if self.replace_whitespace:
            text = _spaces_only(text)
        return text

    def _split(self, text):
        if self.break_on_hyphens is True:
            chunks = _wordsep_re.split(text)
        else:
            chunks = _wordsep_simple_re.split(text)
        return [c for c in chunks if c]

    def _fix_sentence_endings(self, chunks):
        i = 0
        while i < len(chunks) - 1:
            if chunks[i + 1] == " " and _sentence_end_re.search(chunks[i]):
                chunks[i + 1] = "  "
                i += 2
            else:
                i += 1

    def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
        if width < 1:
            space_left = 1
        else:
            space_left = width - cur_len
        if self.break_long_words:
            last = len(reversed_chunks) - 1
            cur_line.append(reversed_chunks[last][:space_left])
            reversed_chunks[last] = reversed_chunks[last][space_left:]
        elif not cur_line:
            cur_line.append(reversed_chunks.pop())

    def _wrap_chunks(self, chunks):
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        if self.max_lines is not None:
            if self.max_lines > 1:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            if len(indent) + len(self.placeholder.lstrip()) > self.width:
                raise ValueError("placeholder too large for max width")
        # (The chunks are taken from the end of the list: it's turned round.)
        chunks.reverse()
        while chunks:
            cur_line = []
            cur_len = 0
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            width = self.width - len(indent)
            if self.drop_whitespace and chunks[-1].strip() == "" and lines:
                chunks.pop()
            while chunks:
                l = len(chunks[-1])
                if cur_len + l <= width:
                    cur_line.append(chunks.pop())
                    cur_len += l
                else:
                    break
            if chunks and len(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)
                cur_len = sum([len(c) for c in cur_line])
            if self.drop_whitespace and cur_line and cur_line[-1].strip() == "":
                cur_len -= len(cur_line[-1])
                cur_line.pop()
            if cur_line:
                if (self.max_lines is None or len(lines) + 1 < self.max_lines or
                        (not chunks or self.drop_whitespace and len(chunks) == 1 and not chunks[0].strip())
                        and cur_len <= width):
                    lines.append(indent + "".join(cur_line))
                else:
                    placed = False
                    while cur_line:
                        if cur_line[-1].strip() and cur_len + len(self.placeholder) <= width:
                            cur_line.append(self.placeholder)
                            lines.append(indent + "".join(cur_line))
                            placed = True
                            break
                        cur_len -= len(cur_line[-1])
                        cur_line.pop()
                    if not placed:
                        joined = False
                        if lines:
                            prev_line = lines[-1].rstrip()
                            if len(prev_line) + len(self.placeholder) <= self.width:
                                lines[-1] = prev_line + self.placeholder
                                joined = True
                        if not joined:
                            lines.append(indent + self.placeholder.lstrip())
                    break
        return lines

    def _split_chunks(self, text):
        return self._split(self._munge_whitespace(text))

    def wrap(self, text):
        """The text's words on lines of at most `width` characters."""
        chunks = self._split_chunks(text)
        if self.fix_sentence_endings:
            self._fix_sentence_endings(chunks)
        return self._wrap_chunks(chunks)

    def fill(self, text):
        """The wrapped lines, as one text."""
        return "\n".join(self.wrap(text))


def wrap(text, width=70, **kwargs):
    """A paragraph as a list of lines of at most `width` characters."""
    return TextWrapper(width=width, **kwargs).wrap(text)


def fill(text, width=70, **kwargs):
    """A paragraph wrapped to `width` characters, as one text."""
    return TextWrapper(width=width, **kwargs).fill(text)


def shorten(text, width, **kwargs):
    """The text on one line of at most `width` characters, cut with [...] if it's longer."""
    w = TextWrapper(width=width, max_lines=1, **kwargs)
    return w.fill(" ".join(text.strip().split()))


_whitespace_only_re = re.compile("^[ \t]+$", re.MULTILINE)
_leading_whitespace_re = re.compile("(^[ \t]*)(?:[^ \t\n])", re.MULTILINE)


def dedent(text):
    """The text without the white space every line starts with."""
    margin = None
    text = _whitespace_only_re.sub("", text)
    indents = _leading_whitespace_re.findall(text)
    for indent in indents:
        if margin is None:
            margin = indent
        elif indent.startswith(margin):
            pass
        elif margin.startswith(indent):
            margin = indent
        else:
            # The part they both start with.
            i = 0
            while i < len(margin) and i < len(indent) and margin[i] == indent[i]:
                i += 1
            margin = margin[:i]
    if margin:
        text = re.sub(r"(?m)^" + margin, "", text)
    return text


def indent(text, prefix, predicate=None):
    """The text with `prefix` before each line (each that isn't only white space)."""
    out = []
    for line in _lines_with_ends(text):
        if predicate is None:
            wanted = line.strip()
        else:
            wanted = predicate(line)
        out.append(prefix + line if wanted else line)
    return "".join(out)
