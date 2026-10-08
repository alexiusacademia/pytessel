# datetime: dates, times of day, moments, and the time between two of them.
#
# Author: Alexius Academia
# Date: 2026-10-08
#
# After CPython's own Python version of the module. A date is kept as its
# year, month and day; a timedelta as days, seconds and microseconds. The
# clock and the computer's time zone come from the built-in modules time
# and _pytessel.
import time as _time
import math as _math
import _pytessel

MINYEAR = 1
MAXYEAR = 9999
_MAXORDINAL = 3652059

_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_DAYS_BEFORE_MONTH = [-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
_MONTHNAMES = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_DAYNAMES = [None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_FULL_MONTHS = [None, "January", "February", "March", "April", "May", "June", "July", "August", "September",
                "October", "November", "December"]
_FULL_DAYS = [None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_before_year(year):
    # How many days there are before 1 January of a year.
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


def _days_in_month(year, month):
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


def _days_before_month(year, month):
    if month > 2 and _is_leap(year):
        return _DAYS_BEFORE_MONTH[month] + 1
    return _DAYS_BEFORE_MONTH[month]


def _ymd2ord(year, month, day):
    # A date's number: 1 for 1 January of year 1.
    return _days_before_year(year) + _days_before_month(year, month) + day


_DI400Y = _days_before_year(401)
_DI100Y = _days_before_year(101)
_DI4Y = _days_before_year(5)


def _ord2ymd(n):
    # The (year, month, day) of a date's number.
    n -= 1
    n400, n = divmod(n, _DI400Y)
    year = n400 * 400 + 1
    n100, n = divmod(n, _DI100Y)
    n4, n = divmod(n, _DI4Y)
    n1, n = divmod(n, 365)
    year += n100 * 100 + n4 * 4 + n1
    if n1 == 4 or n100 == 4:
        return year - 1, 12, 31
    leapyear = n1 == 3 and (n4 != 24 or n100 == 3)
    month = (n + 50) >> 5
    preceding = _DAYS_BEFORE_MONTH[month] + (1 if month > 2 and leapyear else 0)
    if preceding > n:
        month -= 1
        preceding -= _DAYS_IN_MONTH[month] + (1 if month == 2 and leapyear else 0)
    n -= preceding
    return year, month, n + 1


def _type_name(x):
    # A value's type as Python's error messages name it.
    if isinstance(x, datetime):
        return "datetime.datetime"
    if isinstance(x, date):
        return "datetime.date"
    if isinstance(x, timedelta):
        return "datetime.timedelta"
    if isinstance(x, time):
        return "datetime.time"
    if isinstance(x, timezone):
        return "datetime.timezone"
    return type(x).__name__


def _unsupported(symbol, a, b):
    return TypeError("unsupported operand type(s) for %s: '%s' and '%s'" % (symbol, _type_name(a), _type_name(b)))


def _unordered(symbol, a, b):
    return TypeError("'%s' not supported between instances of '%s' and '%s'" % (symbol, _type_name(a), _type_name(b)))


def _index(value):
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        raise TypeError("integer argument expected, got float")
    raise TypeError("an integer is required (got type %s)" % type(value).__name__)


def _check_date_fields(year, month, day):
    year = _index(year)
    month = _index(month)
    day = _index(day)
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError("year %d is out of range" % year)
    if not 1 <= month <= 12:
        raise ValueError("month must be in 1..12")
    if not 1 <= day <= _days_in_month(year, month):
        raise ValueError("day is out of range for month")
    return year, month, day


def _check_time_fields(hour, minute, second, microsecond, fold):
    hour = _index(hour)
    minute = _index(minute)
    second = _index(second)
    microsecond = _index(microsecond)
    if not 0 <= hour <= 23:
        raise ValueError("hour must be in 0..23")
    if not 0 <= minute <= 59:
        raise ValueError("minute must be in 0..59")
    if not 0 <= second <= 59:
        raise ValueError("second must be in 0..59")
    if not 0 <= microsecond <= 999999:
        raise ValueError("microsecond must be in 0..999999")
    if fold not in (0, 1):
        raise ValueError("fold must be either 0 or 1")
    return hour, minute, second, microsecond, fold


def _check_tzinfo(tz):
    if tz is not None and not isinstance(tz, tzinfo):
        raise TypeError("tzinfo argument must be None or of a tzinfo subclass, not type '%s'" % type(tz).__name__)


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def _divide_and_round(a, b):
    # a / b, to the nearest whole number (a half goes to the even one).
    q, r = divmod(a, b)
    r *= 2
    greater_than_half = r > b if b > 0 else r < b
    if greater_than_half or r == b and q % 2 == 1:
        q += 1
    return q


_TIME_SPECS = {
    "hours": "{:02d}",
    "minutes": "{:02d}:{:02d}",
    "seconds": "{:02d}:{:02d}:{:02d}",
    "milliseconds": "{:02d}:{:02d}:{:02d}.{:03d}",
    "microseconds": "{:02d}:{:02d}:{:02d}.{:06d}",
}


def _format_time(hh, mm, ss, us, timespec="auto"):
    if timespec == "auto":
        timespec = "microseconds" if us else "seconds"
    elif timespec == "milliseconds":
        us = us // 1000
    if timespec not in _TIME_SPECS:
        raise ValueError("Unknown timespec value")
    return _TIME_SPECS[timespec].format(hh, mm, ss, us)


def _format_offset(off, sep=":"):
    # A distance from UTC: +05:30. Nothing for None.
    if off is None:
        return ""
    sign = "+"
    if off.days < 0:
        sign = "-"
        off = -off
    seconds = off.days * 86400 + off.seconds
    hh, rest = divmod(seconds, 3600)
    mm, ss = divmod(rest, 60)
    s = "%s%02d%s%02d" % (sign, hh, sep, mm)
    if ss or off.microseconds:
        s += "%s%02d" % (sep, ss)
        if off.microseconds:
            s += ".%06d" % off.microseconds
    return s


# ---- strftime ----

def _strftime(obj, fmt, y, m, d, hh, mi, ss, us):
    if not isinstance(fmt, str):
        raise TypeError("strftime() argument 1 must be str, not %s" % type(fmt).__name__)
    if "%" not in fmt:
        return fmt
    ordinal = _ymd2ord(y, m, d)
    weekday = (ordinal + 6) % 7
    yday = _days_before_month(y, m) + d
    out = []
    size = len(fmt)
    i = 0
    while i < size:
        c = fmt[i]
        i += 1
        if c != "%":
            out.append(c)
            continue
        if i >= size:
            out.append("%")
            break
        c = fmt[i]
        i += 1
        if c == "Y":
            out.append("%04d" % y)
        elif c == "m":
            out.append("%02d" % m)
        elif c == "d":
            out.append("%02d" % d)
        elif c == "H":
            out.append("%02d" % hh)
        elif c == "M":
            out.append("%02d" % mi)
        elif c == "S":
            out.append("%02d" % ss)
        elif c == "f":
            out.append("%06d" % us)
        elif c == "y":
            out.append("%02d" % (y % 100))
        elif c == "b" or c == "h":
            out.append(_MONTHNAMES[m])
        elif c == "B":
            out.append(_FULL_MONTHS[m])
        elif c == "a":
            out.append(_DAYNAMES[weekday + 1])
        elif c == "A":
            out.append(_FULL_DAYS[weekday + 1])
        elif c == "j":
            out.append("%03d" % yday)
        elif c == "p":
            out.append("AM" if hh < 12 else "PM")
        elif c == "I":
            out.append("%02d" % (hh % 12 or 12))
        elif c == "%":
            out.append("%")
        elif c == "z":
            off = obj.utcoffset() if hasattr(obj, "utcoffset") else None
            out.append(_format_offset(off, ""))
        elif c == "Z":
            name = obj.tzname() if hasattr(obj, "tzname") else None
            out.append(name or "")
        elif c == "c":
            out.append("%s %s %2d %02d:%02d:%02d %04d" % (_DAYNAMES[weekday + 1], _MONTHNAMES[m], d, hh, mi, ss, y))
        elif c == "x" or c == "D":
            out.append("%02d/%02d/%02d" % (m, d, y % 100))
        elif c == "X" or c == "T":
            out.append("%02d:%02d:%02d" % (hh, mi, ss))
        elif c == "R":
            out.append("%02d:%02d" % (hh, mi))
        elif c == "F":
            out.append("%04d-%02d-%02d" % (y, m, d))
        elif c == "e":
            out.append("%2d" % d)
        elif c == "w":
            out.append(str((weekday + 1) % 7))
        elif c == "u":
            out.append(str(weekday + 1))
        elif c == "U":
            out.append("%02d" % ((yday + 6 - (weekday + 1) % 7) // 7))
        elif c == "W":
            out.append("%02d" % ((yday + 6 - weekday) // 7))
        elif c == "G":
            out.append("%04d" % date(y, m, d).isocalendar()[0])
        elif c == "V":
            out.append("%02d" % date(y, m, d).isocalendar()[1])
        elif c == "C":
            out.append("%02d" % (y // 100))
        elif c == "n":
            out.append("\n")
        elif c == "t":
            out.append("\t")
        else:
            out.append("%" + c)
    return "".join(out)


# ---- timedelta ----

def _td_part(value, name):
    # A part of a timedelta as (whole number, the rest as a float).
    if isinstance(value, int):
        return int(value), 0.0
    if isinstance(value, float):
        if value != value:
            raise ValueError("cannot convert float NaN to integer")
        if value - value != 0.0:
            raise OverflowError("cannot convert float infinity to integer")
        whole = int(value)
        return whole, value - whole
    raise TypeError("unsupported type for timedelta %s component: %s" % (name, type(value).__name__))


class timedelta:
    """The time between two moments: days, seconds and microseconds."""

    __module__ = "datetime"

    def __init__(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        d = 0
        s = 0
        us = 0
        # What's less than a whole unit of a float, in seconds and in microseconds.
        fs = 0.0
        fus = 0.0
        whole, rest = _td_part(days, "days")
        d += whole
        fs += rest * 86400.0
        whole, rest = _td_part(weeks, "weeks")
        d += whole * 7
        fs += rest * 604800.0
        whole, rest = _td_part(hours, "hours")
        s += whole * 3600
        fs += rest * 3600.0
        whole, rest = _td_part(minutes, "minutes")
        s += whole * 60
        fs += rest * 60.0
        whole, rest = _td_part(seconds, "seconds")
        s += whole
        fs += rest
        # (A float of microseconds is rounded as a whole, with the rest.)
        if isinstance(milliseconds, float):
            _td_part(milliseconds, "milliseconds")
            fus += milliseconds * 1000.0
        else:
            us += _td_part(milliseconds, "milliseconds")[0] * 1000
        if isinstance(microseconds, float):
            _td_part(microseconds, "microseconds")
            fus += microseconds
        else:
            us += _td_part(microseconds, "microseconds")[0]
        if fs != 0.0:
            whole = int(fs)
            s += whole
            fus += (fs - whole) * 1000000.0
        if fus != 0.0:
            if abs(fus) > 8.0e18:
                raise OverflowError("Python int too large to convert to C int")
            us += round(fus)
        carry, us = divmod(us, 1000000)
        s += carry
        carry, s = divmod(s, 86400)
        d += carry
        if abs(d) > 999999999:
            raise OverflowError("days=%d; must have magnitude <= 999999999" % d)
        self._days = d
        self._seconds = s
        self._microseconds = us

    @property
    def days(self):
        return self._days

    @property
    def seconds(self):
        return self._seconds

    @property
    def microseconds(self):
        return self._microseconds

    def _to_microseconds(self):
        return (self._days * 86400 + self._seconds) * 1000000 + self._microseconds

    def total_seconds(self):
        """The whole of it, in seconds."""
        seconds = self._days * 86400 + self._seconds
        if self._microseconds == 0:
            return float(seconds)
        if abs(self._days) < 100000000:
            return (seconds * 1000000 + self._microseconds) / 1000000
        return seconds + self._microseconds / 1000000

    def __repr__(self):
        args = []
        if self._days:
            args.append("days=%d" % self._days)
        if self._seconds:
            args.append("seconds=%d" % self._seconds)
        if self._microseconds:
            args.append("microseconds=%d" % self._microseconds)
        if not args:
            args.append("0")
        return "datetime.timedelta(%s)" % ", ".join(args)

    def __str__(self):
        mm, ss = divmod(self._seconds, 60)
        hh, mm = divmod(mm, 60)
        s = "%d:%02d:%02d" % (hh, mm, ss)
        if self._days:
            s = "%d day%s, " % (self._days, "" if abs(self._days) == 1 else "s") + s
        if self._microseconds:
            s = s + ".%06d" % self._microseconds
        return s

    def __add__(self, other):
        if isinstance(other, timedelta):
            return timedelta(self._days + other._days, self._seconds + other._seconds,
                             self._microseconds + other._microseconds)
        if isinstance(other, (date, datetime)):
            return other + self
        raise _unsupported("+", self, other)

    def __radd__(self, other):
        raise _unsupported("+", other, self)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return timedelta(self._days - other._days, self._seconds - other._seconds,
                             self._microseconds - other._microseconds)
        raise _unsupported("-", self, other)

    def __rsub__(self, other):
        raise _unsupported("-", other, self)

    def __neg__(self):
        return timedelta(-self._days, -self._seconds, -self._microseconds)

    def __pos__(self):
        return self

    def __abs__(self):
        if self._days < 0:
            return -self
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            return timedelta(self._days * other, self._seconds * other, self._microseconds * other)
        if isinstance(other, float):
            return timedelta(self._days * other, self._seconds * other, self._microseconds * other)
        if isinstance(other, (str, list, tuple)):
            raise TypeError("can't multiply sequence by non-int of type 'datetime.timedelta'")
        raise _unsupported("*", self, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self * other
        if isinstance(other, (str, list, tuple)):
            raise TypeError("can't multiply sequence by non-int of type 'datetime.timedelta'")
        raise _unsupported("*", other, self)

    def __floordiv__(self, other):
        if isinstance(other, timedelta):
            theirs = other._to_microseconds()
            if theirs == 0:
                raise ZeroDivisionError("integer division or modulo by zero")
            return self._to_microseconds() // theirs
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("integer division or modulo by zero")
            return timedelta(0, 0, self._to_microseconds() // other)
        raise _unsupported("//", self, other)

    def __truediv__(self, other):
        if isinstance(other, timedelta):
            theirs = other._to_microseconds()
            if theirs == 0:
                raise ZeroDivisionError("division by zero")
            return self._to_microseconds() / theirs
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("integer division or modulo by zero")
            return timedelta(0, 0, _divide_and_round(self._to_microseconds(), other))
        if isinstance(other, float):
            if other == 0.0:
                raise ZeroDivisionError("float division by zero")
            return timedelta(0, 0, self._to_microseconds() / other)
        raise _unsupported("/", self, other)

    def __mod__(self, other):
        if isinstance(other, timedelta):
            theirs = other._to_microseconds()
            if theirs == 0:
                raise ZeroDivisionError("integer division or modulo by zero")
            return timedelta(0, 0, self._to_microseconds() % theirs)
        raise _unsupported("%", self, other)

    def __divmod__(self, other):
        if isinstance(other, timedelta):
            q, r = divmod(self._to_microseconds(), other._to_microseconds())
            return q, timedelta(0, 0, r)
        raise _unsupported("divmod()", self, other)

    def _key(self):
        return (self._days, self._seconds, self._microseconds)

    def __eq__(self, other):
        return isinstance(other, timedelta) and self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if not isinstance(other, timedelta):
            raise _unordered("<", self, other)
        return self._key() < other._key()

    def __le__(self, other):
        if not isinstance(other, timedelta):
            raise _unordered("<=", self, other)
        return self._key() <= other._key()

    def __gt__(self, other):
        if not isinstance(other, timedelta):
            raise _unordered(">", self, other)
        return self._key() > other._key()

    def __ge__(self, other):
        if not isinstance(other, timedelta):
            raise _unordered(">=", self, other)
        return self._key() >= other._key()

    def __bool__(self):
        return self._days != 0 or self._seconds != 0 or self._microseconds != 0

    def __hash__(self):
        return hash(("timedelta", self._days, self._seconds, self._microseconds))


timedelta.min = timedelta(-999999999)
timedelta.max = timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)
timedelta.resolution = timedelta(microseconds=1)


# ---- date ----

class _IsoCalendarDate:
    """What isocalendar() gives: a (year, week, weekday) with names."""

    def __init__(self, year, week, weekday):
        self.year = year
        self.week = week
        self.weekday = weekday

    def _values(self):
        return (self.year, self.week, self.weekday)

    def __repr__(self):
        return "datetime.IsoCalendarDate(year=%d, week=%d, weekday=%d)" % self._values()

    def __iter__(self):
        return iter(self._values())

    def __len__(self):
        return 3

    def __getitem__(self, index):
        return self._values()[index]

    def __eq__(self, other):
        if isinstance(other, _IsoCalendarDate):
            return self._values() == other._values()
        return self._values() == other

    def __hash__(self):
        return hash(self._values())


def _isoweek1monday(year):
    # The number of the Monday that starts a year's first ISO week.
    firstday = _ymd2ord(year, 1, 1)
    firstweekday = (firstday + 6) % 7
    week1monday = firstday - firstweekday
    if firstweekday > 3:
        week1monday += 7
    return week1monday


def _two_digits(text):
    if len(text) != 2 or not text.isdigit():
        raise ValueError("not two digits")
    return int(text)


def _parse_isoformat_date(text):
    if len(text) != 10 or text[4] != "-" or text[7] != "-" or not text[0:4].isdigit():
        raise ValueError("Invalid date")
    return [int(text[0:4]), _two_digits(text[5:7]), _two_digits(text[8:10])]


def _parse_hh_mm_ss_ff(text):
    size = len(text)
    parts = [0, 0, 0, 0]
    pos = 0
    for part in range(0, 3):
        if size - pos < 2:
            raise ValueError("Incomplete time component")
        parts[part] = _two_digits(text[pos:pos + 2])
        pos += 2
        next_char = text[pos:pos + 1]
        if not next_char or part >= 2:
            break
        if next_char != ":":
            raise ValueError("Invalid time separator: %s" % next_char)
        pos += 1
    if pos < size:
        if text[pos] != ".":
            raise ValueError("Invalid microsecond component")
        pos += 1
        rest = text[pos:]
        if len(rest) not in (3, 6) or not rest.isdigit():
            raise ValueError("Invalid microsecond component")
        parts[3] = int(rest)
        if len(rest) == 3:
            parts[3] *= 1000
    return parts


def _parse_isoformat_time(text):
    # Gives [hour, minute, second, microsecond, tzinfo].
    if len(text) < 2:
        raise ValueError("Isoformat time too short")
    tz_pos = text.find("-") + 1 or text.find("+") + 1
    timestr = text[:tz_pos - 1] if tz_pos > 0 else text
    parts = _parse_hh_mm_ss_ff(timestr)
    tzi = None
    if tz_pos > 0:
        tzstr = text[tz_pos:]
        if len(tzstr) not in (5, 8, 15):
            raise ValueError("Malformed time zone string")
        tz_parts = _parse_hh_mm_ss_ff(tzstr)
        if tz_parts == [0, 0, 0, 0]:
            tzi = timezone.utc
        else:
            td = timedelta(hours=tz_parts[0], minutes=tz_parts[1], seconds=tz_parts[2], microseconds=tz_parts[3])
            if text[tz_pos - 1] == "-":
                td = -td
            tzi = timezone(td)
    parts.append(tzi)
    return parts


class date:
    """A day of the calendar: date(2024, 5, 17)."""

    __module__ = "datetime"

    def __init__(self, year, month, day):
        year, month, day = _check_date_fields(year, month, day)
        self._year = year
        self._month = month
        self._day = day

    @classmethod
    def fromtimestamp(cls, t):
        """The date, here, of a time in seconds since 1970."""
        seconds = _math.floor(t)
        seconds += _pytessel.utc_offset(seconds)
        y, m, d = _ord2ymd(719163 + seconds // 86400)
        return cls(y, m, d)

    @classmethod
    def today(cls):
        return cls.fromtimestamp(_time.time())

    @classmethod
    def fromordinal(cls, n):
        """The date of a day's number, where 1 January of year 1 is day 1."""
        n = _index(n)
        if n < 1:
            raise ValueError("ordinal must be >= 1")
        if n > _MAXORDINAL:
            raise ValueError("year %d is out of range" % (_ord2ymd(n)[0]))
        y, m, d = _ord2ymd(n)
        return cls(y, m, d)

    @classmethod
    def fromisoformat(cls, date_string):
        """A date from the text isoformat() gives: 2024-05-17."""
        if not isinstance(date_string, str):
            raise TypeError("fromisoformat: argument must be str")
        try:
            parts = _parse_isoformat_date(date_string)
        except ValueError:
            raise ValueError("Invalid isoformat string: %r" % date_string)
        return cls(parts[0], parts[1], parts[2])

    @classmethod
    def fromisocalendar(cls, year, week, day):
        """The date of a year, a week's number and a weekday (1 is Monday)."""
        if not MINYEAR <= year <= MAXYEAR:
            raise ValueError("Year is out of range: %d" % year)
        if not 0 < week < 53:
            out_of_range = True
            if week == 53:
                first_weekday = _ymd2ord(year, 1, 1) % 7
                if first_weekday == 4 or (first_weekday == 3 and _is_leap(year)):
                    out_of_range = False
            if out_of_range:
                raise ValueError("Invalid week: %d" % week)
        if not 0 < day < 8:
            raise ValueError("Invalid weekday: %d (range is [1, 7])" % day)
        y, m, d = _ord2ymd(_isoweek1monday(year) + (week - 1) * 7 + day - 1)
        return cls(y, m, d)

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    def __repr__(self):
        return "datetime.date(%d, %d, %d)" % (self._year, self._month, self._day)

    def ctime(self):
        weekday = self.toordinal() % 7 or 7
        return "%s %s %2d 00:00:00 %04d" % (_DAYNAMES[weekday], _MONTHNAMES[self._month], self._day, self._year)

    def strftime(self, fmt):
        """The date as text, written the way `fmt` says: %Y-%m-%d."""
        return _strftime(self, fmt, self._year, self._month, self._day, 0, 0, 0, 0)

    def __format__(self, fmt):
        if not isinstance(fmt, str):
            raise TypeError("must be str, not %s" % type(fmt).__name__)
        if len(fmt) != 0:
            return self.strftime(fmt)
        return str(self)

    def isoformat(self):
        return "%04d-%02d-%02d" % (self._year, self._month, self._day)

    def __str__(self):
        return self.isoformat()

    def timetuple(self):
        """(year, month, day, 0, 0, 0, weekday, day of the year, -1)."""
        yday = _days_before_month(self._year, self._month) + self._day
        return (self._year, self._month, self._day, 0, 0, 0, self.weekday(), yday, -1)

    def toordinal(self):
        """The day's number, where 1 January of year 1 is day 1."""
        return _ymd2ord(self._year, self._month, self._day)

    def replace(self, year=None, month=None, day=None):
        """A date with some of its parts changed."""
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        return type(self)(year, month, day)

    def _key(self):
        return (self._year, self._month, self._day)

    def _other_date(self, other, symbol):
        # The other side of a comparison, which must be a date too.
        if isinstance(other, datetime) or isinstance(self, datetime):
            if isinstance(other, date):
                raise TypeError("can't compare datetime.datetime to datetime.date")
        if not isinstance(other, date):
            raise _unordered(symbol, self, other)
        return other._key()

    def __eq__(self, other):
        return isinstance(other, date) and not isinstance(other, datetime) and self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self._key() < self._other_date(other, "<")

    def __le__(self, other):
        return self._key() <= self._other_date(other, "<=")

    def __gt__(self, other):
        return self._key() > self._other_date(other, ">")

    def __ge__(self, other):
        return self._key() >= self._other_date(other, ">=")

    def __hash__(self):
        return hash(("date", self._year, self._month, self._day))

    def __add__(self, other):
        if isinstance(other, timedelta):
            o = self.toordinal() + other.days
            if 0 < o <= _MAXORDINAL:
                return type(self).fromordinal(o)
            raise OverflowError("date value out of range")
        raise _unsupported("+", self, other)

    def __radd__(self, other):
        raise _unsupported("+", other, self)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self + timedelta(-other.days)
        if isinstance(other, date) and not isinstance(other, datetime):
            return timedelta(self.toordinal() - other.toordinal())
        raise _unsupported("-", self, other)

    def __rsub__(self, other):
        raise _unsupported("-", other, self)

    def weekday(self):
        """The day of the week: 0 for Monday to 6 for Sunday."""
        return (self.toordinal() + 6) % 7

    def isoweekday(self):
        """The day of the week: 1 for Monday to 7 for Sunday."""
        return self.toordinal() % 7 or 7

    def isocalendar(self):
        """(ISO year, week's number, weekday)."""
        year = self._year
        week1monday = _isoweek1monday(year)
        today = _ymd2ord(self._year, self._month, self._day)
        week, day = divmod(today - week1monday, 7)
        if week < 0:
            year -= 1
            week1monday = _isoweek1monday(year)
            week, day = divmod(today - week1monday, 7)
        elif week >= 52:
            if today >= _isoweek1monday(year + 1):
                year += 1
                week = 0
        return _IsoCalendarDate(year, week + 1, day + 1)


date.min = date(1, 1, 1)
date.max = date(9999, 12, 31)
date.resolution = timedelta(days=1)


# ---- tzinfo and timezone ----

class tzinfo:
    """A time zone: a class of your own says what utcoffset(), tzname() and dst() are."""

    __module__ = "datetime"

    def tzname(self, dt):
        raise NotImplementedError("a tzinfo subclass must implement tzname()")

    def utcoffset(self, dt):
        raise NotImplementedError("a tzinfo subclass must implement utcoffset()")

    def dst(self, dt):
        raise NotImplementedError("a tzinfo subclass must implement dst()")

    def fromutc(self, dt):
        if not isinstance(dt, datetime):
            raise TypeError("fromutc() requires a datetime argument")
        if dt.tzinfo is not self:
            raise ValueError("dt.tzinfo is not self")
        dtoff = dt.utcoffset()
        if dtoff is None:
            raise ValueError("fromutc() requires a non-None utcoffset() result")
        dtdst = dt.dst()
        if dtdst is None:
            raise ValueError("fromutc() requires a non-None dst() result")
        delta = dtoff - dtdst
        if delta:
            dt += delta
            dtdst = dt.dst()
            if dtdst is None:
                raise ValueError("fromutc(): dt.dst gave inconsistent results; cannot convert")
        return dt + dtdst


class timezone(tzinfo):
    """A time zone that's always the same distance from UTC."""

    __module__ = "datetime"

    def __init__(self, offset, name=None):
        if not isinstance(offset, timedelta):
            raise TypeError("timezone() argument 1 must be datetime.timedelta, not %s" % type(offset).__name__)
        if name is not None and not isinstance(name, str):
            raise TypeError("name must be a string")
        if not (timedelta(days=-1) < offset and offset < timedelta(days=1)):
            raise ValueError("offset must be a timedelta strictly between -timedelta(hours=24) and "
                             "timedelta(hours=24), not %r." % (offset,))
        self._offset = offset
        self._name = name

    def __eq__(self, other):
        return isinstance(other, timezone) and self._offset == other._offset

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._offset)

    def __repr__(self):
        if self._name is None:
            if not self._offset:
                return "datetime.timezone.utc"
            return "datetime.timezone(%r)" % (self._offset,)
        return "datetime.timezone(%r, %r)" % (self._offset, self._name)

    def __str__(self):
        return self.tzname(None)

    def utcoffset(self, dt):
        if isinstance(dt, datetime) or dt is None:
            return self._offset
        raise TypeError("utcoffset() argument must be a datetime instance or None")

    def tzname(self, dt):
        if isinstance(dt, datetime) or dt is None:
            if self._name is None:
                return self._name_from_offset(self._offset)
            return self._name
        raise TypeError("tzname() argument must be a datetime instance or None")

    def dst(self, dt):
        if isinstance(dt, datetime) or dt is None:
            return None
        raise TypeError("dst() argument must be a datetime instance or None")

    def fromutc(self, dt):
        if isinstance(dt, datetime):
            if dt.tzinfo is not self:
                raise ValueError("fromutc: dt.tzinfo is not self")
            return dt + self._offset
        raise TypeError("fromutc() argument must be a datetime instance or None")

    def _name_from_offset(self, delta):
        if not delta:
            return "UTC"
        return "UTC" + _format_offset(delta)


timezone.utc = timezone(timedelta(0))
timezone.min = timezone(timedelta(hours=-23, minutes=-59))
timezone.max = timezone(timedelta(hours=23, minutes=59))
UTC = timezone.utc


# ---- time ----

class time:
    """A time of day: time(13, 30)."""

    __module__ = "datetime"

    def __init__(self, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, fold=0):
        hour, minute, second, microsecond, fold = _check_time_fields(hour, minute, second, microsecond, fold)
        _check_tzinfo(tzinfo)
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._fold = fold

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    @property
    def microsecond(self):
        return self._microsecond

    @property
    def tzinfo(self):
        return self._tzinfo

    @property
    def fold(self):
        return self._fold

    def _key(self):
        return (self._hour, self._minute, self._second, self._microsecond)

    def _compare(self, other, symbol, equality=False):
        # -1, 0 or 1, as self is before, the same as or after other
        # (2 when they can't be compared, and it's only == that asks).
        if not isinstance(other, time):
            raise _unordered(symbol, self, other)
        mytz = self._tzinfo
        ottz = other._tzinfo
        myoff = None
        otoff = None
        if mytz is ottz:
            base_compare = True
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            base_compare = myoff == otoff
        if base_compare:
            return _cmp(self._key(), other._key())
        if myoff is None or otoff is None:
            if equality:
                return 2
            raise TypeError("can't compare offset-naive and offset-aware times")
        mine = self._hour * 3600 + self._minute * 60 + self._second - (myoff.days * 86400 + myoff.seconds)
        theirs = other._hour * 3600 + other._minute * 60 + other._second - (otoff.days * 86400 + otoff.seconds)
        return _cmp((mine, self._microsecond), (theirs, other._microsecond))

    def __eq__(self, other):
        return isinstance(other, time) and self._compare(other, "==", True) == 0

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self._compare(other, "<") < 0

    def __le__(self, other):
        return self._compare(other, "<=") <= 0

    def __gt__(self, other):
        return self._compare(other, ">") > 0

    def __ge__(self, other):
        return self._compare(other, ">=") >= 0

    def __hash__(self):
        off = self.utcoffset()
        if off is None:
            return hash(("time", self._hour, self._minute, self._second, self._microsecond))
        seconds = self._hour * 3600 + self._minute * 60 + self._second - (off.days * 86400 + off.seconds)
        return hash(("time at", seconds % 86400, self._microsecond))

    def __add__(self, other):
        raise _unsupported("+", self, other)

    def __sub__(self, other):
        raise _unsupported("-", self, other)

    def __repr__(self):
        if self._microsecond != 0:
            s = ", %d, %d" % (self._second, self._microsecond)
        elif self._second != 0:
            s = ", %d" % self._second
        else:
            s = ""
        s = "datetime.time(%d, %d%s)" % (self._hour, self._minute, s)
        if self._tzinfo is not None:
            s = s[:len(s) - 1] + ", tzinfo=%r" % (self._tzinfo,) + ")"
        if self._fold:
            s = s[:len(s) - 1] + ", fold=1)"
        return s

    def isoformat(self, timespec="auto"):
        """The time as text: 13:30:00, with .ffffff and +HH:MM when there are any."""
        s = _format_time(self._hour, self._minute, self._second, self._microsecond, timespec)
        return s + _format_offset(self.utcoffset())

    def __str__(self):
        return self.isoformat()

    @classmethod
    def fromisoformat(cls, time_string):
        """A time from the text isoformat() gives."""
        if not isinstance(time_string, str):
            raise TypeError("fromisoformat: argument must be str")
        try:
            parts = _parse_isoformat_time(time_string)
        except ValueError:
            raise ValueError("Invalid isoformat string: %r" % time_string)
        return cls(parts[0], parts[1], parts[2], parts[3], parts[4])

    def strftime(self, fmt):
        """The time as text, written the way `fmt` says: %H:%M."""
        return _strftime(self, fmt, 1900, 1, 1, self._hour, self._minute, self._second, self._microsecond)

    def __format__(self, fmt):
        if len(fmt) != 0:
            return self.strftime(fmt)
        return str(self)

    def utcoffset(self):
        if self._tzinfo is None:
            return None
        return self._tzinfo.utcoffset(None)

    def tzname(self):
        if self._tzinfo is None:
            return None
        return self._tzinfo.tzname(None)

    def dst(self):
        if self._tzinfo is None:
            return None
        return self._tzinfo.dst(None)

    def replace(self, hour=None, minute=None, second=None, microsecond=None, tzinfo=True, fold=None):
        """A time with some of its parts changed."""
        if hour is None:
            hour = self._hour
        if minute is None:
            minute = self._minute
        if second is None:
            second = self._second
        if microsecond is None:
            microsecond = self._microsecond
        if tzinfo is True:
            tzinfo = self._tzinfo
        if fold is None:
            fold = self._fold
        return type(self)(hour, minute, second, microsecond, tzinfo, fold)


time.min = time(0, 0, 0)
time.max = time(23, 59, 59, 999999)
time.resolution = timedelta(microseconds=1)


# ---- datetime ----

class datetime(date):
    """A moment: a date and a time of day. datetime(2024, 5, 17, 13, 30)."""

    __module__ = "datetime"

    def __init__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, fold=0):
        year, month, day = _check_date_fields(year, month, day)
        hour, minute, second, microsecond, fold = _check_time_fields(hour, minute, second, microsecond, fold)
        _check_tzinfo(tzinfo)
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._fold = fold

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    @property
    def microsecond(self):
        return self._microsecond

    @property
    def tzinfo(self):
        return self._tzinfo

    @property
    def fold(self):
        return self._fold

    @classmethod
    def _from_seconds(cls, seconds, us, tz):
        # The datetime that many seconds after the start of 1970.
        days, rest = divmod(seconds, 86400)
        ordinal = 719163 + days
        if ordinal < 1 or ordinal > _MAXORDINAL:
            raise ValueError("year %d is out of range" % (1970 + seconds // 31556952))
        y, m, d = _ord2ymd(ordinal)
        hh, rest = divmod(rest, 3600)
        mm, ss = divmod(rest, 60)
        return cls(y, m, d, hh, mm, ss, us, tz)

    @classmethod
    def _split_timestamp(cls, t):
        # A time as (whole seconds, microseconds).
        if not isinstance(t, (int, float)):
            raise TypeError("an integer is required (got type %s)" % type(t).__name__)
        if isinstance(t, int):
            return int(t), 0
        if t != t:
            raise ValueError("Invalid value NaN (not a number)")
        if t > 1.0e14 or t < -1.0e14:
            raise OverflowError("timestamp out of range for platform time_t")
        seconds = _math.floor(t)
        us = round((t - seconds) * 1000000.0)
        if us >= 1000000:
            seconds += 1
            us -= 1000000
        return seconds, us

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        """The datetime of a time in seconds since 1970: here, or in the time zone `tz`."""
        _check_tzinfo(tz)
        seconds, us = cls._split_timestamp(t)
        if tz is None:
            return cls._from_seconds(seconds + _pytessel.utc_offset(seconds), us, None)
        return tz.fromutc(cls._from_seconds(seconds, us, tz))

    @classmethod
    def utcfromtimestamp(cls, t):
        """The datetime, at UTC, of a time in seconds since 1970 (with no time zone)."""
        seconds, us = cls._split_timestamp(t)
        return cls._from_seconds(seconds, us, None)

    @classmethod
    def now(cls, tz=None):
        """The date and time it is now."""
        return cls.fromtimestamp(_time.time(), tz)

    @classmethod
    def today(cls):
        return cls.fromtimestamp(_time.time())

    @classmethod
    def utcnow(cls):
        return cls.utcfromtimestamp(_time.time())

    @classmethod
    def fromordinal(cls, n):
        n = _index(n)
        if n < 1:
            raise ValueError("ordinal must be >= 1")
        if n > _MAXORDINAL:
            raise ValueError("year %d is out of range" % (_ord2ymd(n)[0]))
        y, m, d = _ord2ymd(n)
        return cls(y, m, d)

    @classmethod
    def combine(cls, date, time, tzinfo=True):
        """A datetime from a date and a time."""
        if not isinstance(date, _date_class):
            raise TypeError("combine() argument 1 must be datetime.date, not %s" % type(date).__name__)
        if not isinstance(time, _time_class):
            raise TypeError("combine() argument 2 must be datetime.time, not %s" % type(time).__name__)
        if tzinfo is True:
            tzinfo = time.tzinfo
        return cls(date.year, date.month, date.day, time.hour, time.minute, time.second, time.microsecond,
                   tzinfo, time.fold)

    @classmethod
    def fromisoformat(cls, date_string):
        """A datetime from the text isoformat() gives: 2024-05-17T13:30:00."""
        if not isinstance(date_string, str):
            raise TypeError("fromisoformat: argument must be str")
        try:
            if len(date_string) == 11:
                raise ValueError("no time after the separator")
            parts = _parse_isoformat_date(date_string[0:10])
            rest = date_string[11:]
            if rest:
                parts = parts + _parse_isoformat_time(rest)
            else:
                parts = parts + [0, 0, 0, 0, None]
        except ValueError:
            raise ValueError("Invalid isoformat string: %r" % date_string)
        return cls(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7])

    @classmethod
    def strptime(cls, date_string, format):
        """A datetime read from a text written the way `format` says."""
        return _strptime(cls, date_string, format)

    def timetuple(self):
        """(year, month, day, hour, minute, second, weekday, day of the year, -1)."""
        yday = _days_before_month(self._year, self._month) + self._day
        return (self._year, self._month, self._day, self._hour, self._minute, self._second, self.weekday(), yday, -1)

    def _local_timezone(self):
        if self._tzinfo is None:
            seconds = self._mktime()
        else:
            delta = self - _EPOCH
            seconds = delta.days * 86400 + delta.seconds
        return timezone(timedelta(seconds=_pytessel.utc_offset(seconds)))

    def _mktime(self):
        # The seconds since 1970 of a datetime that's in the computer's time zone.
        t = (self.toordinal() - 719163) * 86400 + self._hour * 3600 + self._minute * 60 + self._second
        a = _pytessel.utc_offset(t)
        u1 = t - a
        t1 = u1 + _pytessel.utc_offset(u1)
        if t1 == t:
            # (Twice the same time, when the clocks go back: `fold` says which.)
            u2 = u1 + (86400 if self._fold else -86400)
            b = _pytessel.utc_offset(u2)
            if a == b:
                return u1
        else:
            b = t1 - u1
        u2 = t - b
        t2 = u2 + _pytessel.utc_offset(u2)
        if t2 == t:
            return u2
        if t1 == t:
            return u1
        if self._fold:
            return min(u1, u2)
        return max(u1, u2)

    def timestamp(self):
        """The seconds since the start of 1970 (UTC), as a float."""
        if self._tzinfo is None:
            return self._mktime() + self._microsecond / 1000000
        return (self - _EPOCH).total_seconds()

    def utctimetuple(self):
        offset = self.utcoffset()
        if offset:
            return (self - offset).timetuple()
        return self.timetuple()

    def date(self):
        """The date part."""
        return _date_class(self._year, self._month, self._day)

    def time(self):
        """The time part, without the time zone."""
        return _time_class(self._hour, self._minute, self._second, self._microsecond, None, self._fold)

    def timetz(self):
        """The time part, with the time zone."""
        return _time_class(self._hour, self._minute, self._second, self._microsecond, self._tzinfo, self._fold)

    def replace(self, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None,
                tzinfo=True, fold=None):
        """A datetime with some of its parts changed."""
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        if hour is None:
            hour = self._hour
        if minute is None:
            minute = self._minute
        if second is None:
            second = self._second
        if microsecond is None:
            microsecond = self._microsecond
        if tzinfo is True:
            tzinfo = self._tzinfo
        if fold is None:
            fold = self._fold
        return type(self)(year, month, day, hour, minute, second, microsecond, tzinfo, fold)

    def astimezone(self, tz=None):
        """The same moment, as another time zone's clock shows it."""
        if tz is None:
            tz = self._local_timezone()
        elif not isinstance(tz, _tzinfo_class):
            raise TypeError("tz argument must be an instance of tzinfo")
        mytz = self._tzinfo
        if mytz is None:
            mytz = self._local_timezone()
            myoffset = mytz.utcoffset(self)
        else:
            myoffset = mytz.utcoffset(self)
            if myoffset is None:
                mytz = self.replace(tzinfo=None)._local_timezone()
                myoffset = mytz.utcoffset(self)
        if tz is mytz:
            return self
        utc = (self - myoffset).replace(tzinfo=tz)
        return tz.fromutc(utc)

    def ctime(self):
        weekday = self.toordinal() % 7 or 7
        return "%s %s %2d %02d:%02d:%02d %04d" % (_DAYNAMES[weekday], _MONTHNAMES[self._month], self._day,
                                                 self._hour, self._minute, self._second, self._year)

    def isoformat(self, sep="T", timespec="auto"):
        """The datetime as text: 2024-05-17T13:30:00."""
        s = "%04d-%02d-%02d" % (self._year, self._month, self._day) + sep
        s += _format_time(self._hour, self._minute, self._second, self._microsecond, timespec)
        return s + _format_offset(self.utcoffset())

    def __repr__(self):
        parts = [self._year, self._month, self._day, self._hour, self._minute, self._second, self._microsecond]
        if parts[6] == 0:
            parts.pop()
            if parts[5] == 0:
                parts.pop()
        s = "datetime.datetime(%s)" % ", ".join([str(p) for p in parts])
        if self._tzinfo is not None:
            s = s[:len(s) - 1] + ", tzinfo=%r" % (self._tzinfo,) + ")"
        if self._fold:
            s = s[:len(s) - 1] + ", fold=1)"
        return s

    def __str__(self):
        return self.isoformat(" ")

    def strftime(self, fmt):
        """The datetime as text, written the way `fmt` says: %Y-%m-%d %H:%M."""
        return _strftime(self, fmt, self._year, self._month, self._day, self._hour, self._minute, self._second,
                         self._microsecond)

    def utcoffset(self):
        """How far from UTC its time zone is, as a timedelta (None with no time zone)."""
        if self._tzinfo is None:
            return None
        return self._tzinfo.utcoffset(self)

    def tzname(self):
        if self._tzinfo is None:
            return None
        return self._tzinfo.tzname(self)

    def dst(self):
        if self._tzinfo is None:
            return None
        return self._tzinfo.dst(self)

    def _key(self):
        return (self._year, self._month, self._day, self._hour, self._minute, self._second, self._microsecond)

    def _compare(self, other, symbol, equality=False):
        if not isinstance(other, datetime):
            if isinstance(other, date):
                raise TypeError("can't compare datetime.datetime to datetime.date")
            raise _unordered(symbol, self, other)
        mytz = self._tzinfo
        ottz = other._tzinfo
        myoff = None
        otoff = None
        if mytz is ottz:
            base_compare = True
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            base_compare = myoff == otoff
        if base_compare:
            return _cmp(self._key(), other._key())
        if myoff is None or otoff is None:
            if equality:
                return 2
            raise TypeError("can't compare offset-naive and offset-aware datetimes")
        diff = self - other
        if diff.days < 0:
            return -1
        return 1 if diff else 0

    def __eq__(self, other):
        return isinstance(other, datetime) and self._compare(other, "==", True) == 0

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self._compare(other, "<") < 0

    def __le__(self, other):
        return self._compare(other, "<=") <= 0

    def __gt__(self, other):
        return self._compare(other, ">") > 0

    def __ge__(self, other):
        return self._compare(other, ">=") >= 0

    def __add__(self, other):
        if not isinstance(other, timedelta):
            raise _unsupported("+", self, other)
        days = self.toordinal() + other.days
        seconds = self._hour * 3600 + self._minute * 60 + self._second + other.seconds
        us = self._microsecond + other.microseconds
        carry, us = divmod(us, 1000000)
        seconds += carry
        carry, seconds = divmod(seconds, 86400)
        days += carry
        if not 0 < days <= _MAXORDINAL:
            raise OverflowError("date value out of range")
        y, m, d = _ord2ymd(days)
        hh, rest = divmod(seconds, 3600)
        mm, ss = divmod(rest, 60)
        return type(self)(y, m, d, hh, mm, ss, us, self._tzinfo)

    def __radd__(self, other):
        raise _unsupported("+", other, self)

    def __sub__(self, other):
        if not isinstance(other, datetime):
            if isinstance(other, timedelta):
                return self + -other
            raise _unsupported("-", self, other)
        secs1 = self._second + self._minute * 60 + self._hour * 3600
        secs2 = other._second + other._minute * 60 + other._hour * 3600
        base = timedelta(self.toordinal() - other.toordinal(), secs1 - secs2, self._microsecond - other._microsecond)
        if self._tzinfo is other._tzinfo:
            return base
        myoff = self.utcoffset()
        otoff = other.utcoffset()
        if myoff == otoff:
            return base
        if myoff is None or otoff is None:
            raise TypeError("can't subtract offset-naive and offset-aware datetimes")
        return base + otoff - myoff

    def __rsub__(self, other):
        raise _unsupported("-", other, self)

    def __hash__(self):
        off = self.utcoffset()
        if off is None:
            return hash(("datetime", self._year, self._month, self._day, self._hour, self._minute, self._second,
                         self._microsecond))
        seconds = self._hour * 3600 + self._minute * 60 + self._second
        at_utc = timedelta(self.toordinal(), seconds, self._microsecond) - off
        return hash(("datetime at", at_utc.days, at_utc.seconds, at_utc.microseconds))


# (Inside datetime, `date` and `time` are its own methods.)
_date_class = date
_time_class = time
_tzinfo_class = tzinfo

datetime.min = datetime(1, 1, 1)
datetime.max = datetime(9999, 12, 31, 23, 59, 59, 999999)
datetime.resolution = timedelta(microseconds=1)
_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


# ---- strptime ----

def _names_pattern(group, names):
    # (name|name|…), the longest names first.
    ordered = sorted([n.lower() for n in names if n], key=len, reverse=True)
    return "(?P<%s>%s)" % (group, "|".join(ordered))


_STRPTIME_PARTS = {
    "d": r"(?P<d>3[0-1]|[1-2]\d|0[1-9]|[1-9]| [1-9])",
    "f": r"(?P<f>[0-9]{1,6})",
    "H": r"(?P<H>2[0-3]|[0-1]\d|\d)",
    "I": r"(?P<I>1[0-2]|0[1-9]|[1-9])",
    "j": r"(?P<j>36[0-6]|3[0-5]\d|[1-2]\d\d|0[1-9]\d|00[1-9]|[1-9]\d|0[1-9]|[1-9])",
    "m": r"(?P<m>1[0-2]|0[1-9]|[1-9])",
    "M": r"(?P<M>[0-5]\d|\d)",
    "S": r"(?P<S>6[0-1]|[0-5]\d|\d)",
    "w": r"(?P<w>[0-6])",
    "u": r"(?P<u>[1-7])",
    "y": r"(?P<y>\d\d)",
    "Y": r"(?P<Y>\d\d\d\d)",
    "z": r"(?P<z>[+-]\d\d:?[0-5]\d(:?[0-5]\d(\.\d{1,6})?)?|(?-i:Z))",
    "A": _names_pattern("A", _FULL_DAYS),
    "a": _names_pattern("a", _DAYNAMES),
    "B": _names_pattern("B", _FULL_MONTHS),
    "b": _names_pattern("b", _MONTHNAMES),
    "p": "(?P<p>am|pm)",
    "Z": "(?P<Z>utc|gmt)",
    "%": "%",
}

_strptime_cache = {}


def _strptime_pattern(format):
    import re
    # %c, %x and %X are other directives put together.
    given = format
    format = format.replace("%%", "\x00").replace("%c", "%a %b %d %H:%M:%S %Y").replace("%x", "%m/%d/%y")
    format = format.replace("%X", "%H:%M:%S").replace("\x00", "%%")
    parts = []
    size = len(format)
    i = 0
    while i < size:
        c = format[i]
        if c == "%":
            if i + 1 >= size:
                raise ValueError("stray %% in format '%s'" % given)
            directive = format[i + 1]
            i += 2
            if directive not in _STRPTIME_PARTS:
                raise ValueError("'%s' is a bad directive in format '%s'" % (directive, given))
            parts.append(_STRPTIME_PARTS[directive])
        elif c in " \t\n\r\x0b\x0c":
            while i < size and format[i] in " \t\n\r\x0b\x0c":
                i += 1
            parts.append("\\s+")
        else:
            parts.append(re.escape(c))
            i += 1
    return re.compile("".join(parts), re.IGNORECASE)


def _strptime(cls, data_string, format):
    if not isinstance(data_string, str):
        raise TypeError("strptime() argument 1 must be str, not %s" % type(data_string).__name__)
    if not isinstance(format, str):
        raise TypeError("strptime() argument 2 must be str, not %s" % type(format).__name__)
    pattern = _strptime_cache.get(format)
    if pattern is None:
        pattern = _strptime_pattern(format)
        _strptime_cache[format] = pattern
    found = pattern.match(data_string)
    if not found:
        raise ValueError("time data %r does not match format %r" % (data_string, format))
    if len(data_string) != found.end():
        raise ValueError("unconverted data remains: %s" % data_string[found.end():])
    year = 1900
    month = 1
    day = 1
    hour = 0
    minute = 0
    second = 0
    fraction = 0
    julian = None
    gmtoff = None
    gmtoff_fraction = 0
    tzname = None
    groups = found.groupdict()
    for key in groups:
        text = groups[key]
        if text is None:
            continue
        if key == "y":
            year = int(text)
            # (Two digits: 69 to 99 are 1969 to 1999, 00 to 68 are 2000 to 2068.)
            if year <= 68:
                year += 2000
            else:
                year += 1900
        elif key == "Y":
            year = int(text)
        elif key == "m":
            month = int(text)
        elif key == "B":
            month = [n.lower() if n else n for n in _FULL_MONTHS].index(text.lower())
        elif key == "b":
            month = [n.lower() if n else n for n in _MONTHNAMES].index(text.lower())
        elif key == "d":
            day = int(text)
        elif key == "H":
            hour = int(text)
        elif key == "I":
            hour = int(text)
            ampm = (groups.get("p") or "").lower()
            if ampm in ("", "am"):
                if hour == 12:
                    hour = 0
            elif hour != 12:
                hour += 12
        elif key == "M":
            minute = int(text)
        elif key == "S":
            second = int(text)
        elif key == "f":
            fraction = int(text + "0" * (6 - len(text)))
        elif key == "j":
            julian = int(text)
        elif key == "z":
            z = text
            if z == "Z":
                gmtoff = 0
            else:
                if z[3] == ":":
                    z = z[:3] + z[4:]
                    if len(z) > 5:
                        if z[5] != ":":
                            raise ValueError("Inconsistent use of : in %s" % text)
                        z = z[:5] + z[6:]
                gmtoff = int(z[1:3]) * 3600 + int(z[3:5]) * 60 + int(z[5:7] or 0)
                rest = z[8:]
                gmtoff_fraction = int(rest + "0" * (6 - len(rest)))
                if z.startswith("-"):
                    gmtoff = -gmtoff
                    gmtoff_fraction = -gmtoff_fraction
        elif key == "Z":
            tzname = text
    if julian is not None:
        found_date = date.fromordinal(julian - 1 + _ymd2ord(year, 1, 1))
        year = found_date.year
        month = found_date.month
        day = found_date.day
    tz = None
    if gmtoff is not None:
        delta = timedelta(seconds=gmtoff, microseconds=gmtoff_fraction)
        if tzname:
            tz = timezone(delta, tzname)
        else:
            tz = timezone(delta)
    return cls(year, month, day, hour, minute, second, fraction, tz)
