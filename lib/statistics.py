# statistics: averages and measures of spread.
#
# Author: Alexius Academia
# Date: 2026-10-08
#
# Python works these out with exact fractions. PyTessel has none: whole
# numbers are added exactly as they are, and floats with math.fsum, which
# gives the sum as if nothing were lost on the way; a division is then
# corrected by what it left over (see _divide). The results are Python's,
# but for a rare last digit.
import math


class StatisticsError(ValueError):
    __module__ = "statistics"


def _numbers(data):
    # The data as a list, checked. Gives (values, whether all are ints).
    values = list(data)
    whole = True
    for x in values:
        if isinstance(x, int):
            continue
        if isinstance(x, float):
            whole = False
            continue
        raise TypeError("can't convert type '%s' to numerator/denominator" % type(x).__name__)
    return values, whole


def _ratio(total, n):
    # total / n for whole numbers: a whole number when it divides evenly.
    if total % n == 0:
        return total // n
    return total / n


def _split(a):
    # A float as two halves that add up to it (each has half its digits).
    c = 134217729.0 * a
    high = c - (c - a)
    return high, a - high


def _divide(terms, n):
    # The sum of some floats divided by n, rounded once: the sum is taken
    # as if nothing were lost, and what the division leaves over (worked
    # out exactly, as Dekker's product does) corrects the quotient.
    q = math.fsum(terms) / n
    if q != q or abs(q) > 1.0e290:
        # (Too large to take apart; or not a number at all.)
        return q
    d = float(n)
    product = q * d
    qh, ql = _split(q)
    dh, dl = _split(d)
    error = ((qh * dh - product) + qh * dl + ql * dh) + ql * dl
    rest = math.fsum(list(terms) + [0.0 - product, 0.0 - error])
    return q + rest / n


def mean(data):
    """The arithmetic mean: the sum divided by how many there are."""
    values, whole = _numbers(data)
    n = len(values)
    if n < 1:
        raise StatisticsError("mean requires at least one data point")
    if whole:
        return _ratio(sum(values), n)
    return _divide(values, n)


def fmean(data):
    """The mean, as a float (faster than mean)."""
    values = list(data)
    n = len(values)
    if n < 1:
        raise StatisticsError("fmean requires at least one data point")
    return math.fsum(values) / n


def geometric_mean(data):
    """The n-th root of the product of n numbers."""
    values = list(data)
    if not values:
        raise StatisticsError("geometric mean requires a non-empty dataset containing positive numbers")
    logs = []
    for x in values:
        if x <= 0:
            raise StatisticsError("geometric mean requires a non-empty dataset containing positive numbers")
        logs.append(math.log(x))
    return math.exp(math.fsum(logs) / len(logs))


def median(data):
    """The middle value (the mean of the two middle ones, for an even count)."""
    values = sorted(data)
    n = len(values)
    if n == 0:
        raise StatisticsError("no median for empty data")
    if n % 2 == 1:
        return values[n // 2]
    i = n // 2
    return (values[i - 1] + values[i]) / 2


def median_low(data):
    """The middle value; of the two middle ones, the smaller."""
    values = sorted(data)
    n = len(values)
    if n == 0:
        raise StatisticsError("no median for empty data")
    if n % 2 == 1:
        return values[n // 2]
    return values[n // 2 - 1]


def median_high(data):
    """The middle value; of the two middle ones, the larger."""
    values = sorted(data)
    n = len(values)
    if n == 0:
        raise StatisticsError("no median for empty data")
    return values[n // 2]


def _counts(data):
    # How many times each value comes, in the order they first come.
    counts = {}
    for x in data:
        counts[x] = counts.get(x, 0) + 1
    return counts


def mode(data):
    """The value that comes most often (the first of them, if several do)."""
    counts = _counts(data)
    if not counts:
        raise StatisticsError("no mode for empty data")
    best = None
    most = 0
    for value in counts:
        if counts[value] > most:
            best = value
            most = counts[value]
    return best


def multimode(data):
    """Every value that comes most often, in the order they first come."""
    counts = _counts(data)
    if not counts:
        return []
    most = max(counts.values())
    return [value for value in counts if counts[value] == most]


def _ss(values, whole, c):
    # The sum of the squares of each value's distance from c (the mean,
    # when c is None): a whole number where it's exact (with True), or
    # the floats that add up to it (with False).
    n = len(values)
    if c is None:
        c = mean(values)
        if whole and isinstance(c, int):
            return sum([(x - c) ** 2 for x in values]), True
        squares = [(x - c) ** 2 for x in values]
        # (The distances should add up to nothing; what they do add up to,
        # from rounding, is taken off.)
        off = math.fsum([x - c for x in values])
        squares.append(0.0 - off * off / n)
        return squares, False
    if whole and isinstance(c, int):
        return sum([(x - c) ** 2 for x in values]), True
    return [float((x - c) ** 2) for x in values], False


def variance(data, xbar=None):
    """The sample variance: for data that's a sample of something larger."""
    values, whole = _numbers(data)
    n = len(values)
    if n < 2:
        raise StatisticsError("variance requires at least two data points")
    total, exact = _ss(values, whole, xbar)
    if exact:
        return _ratio(total, n - 1)
    return _divide(total, n - 1)


def pvariance(data, mu=None):
    """The population variance: for data that's the whole of something."""
    values, whole = _numbers(data)
    n = len(values)
    if n < 1:
        raise StatisticsError("pvariance requires at least one data point")
    total, exact = _ss(values, whole, mu)
    if exact:
        return _ratio(total, n)
    return _divide(total, n)


def stdev(data, xbar=None):
    """The sample standard deviation: the square root of the variance."""
    return math.sqrt(variance(data, xbar))


def pstdev(data, mu=None):
    """The population standard deviation."""
    return math.sqrt(pvariance(data, mu))
