# The statistics module.
#
# Author: Alexius Academia
# Date: 2026-10-08
import statistics
from statistics import (mean, fmean, median, median_low, median_high, mode, multimode, stdev, pstdev,
                        variance, pvariance, StatisticsError)


def attempt(label, function, *args):
    try:
        print(label, function(*args))
    except StatisticsError as e:
        print(label, "StatisticsError:", e)
    except TypeError as e:
        print(label, "TypeError:", e)


# ---- mean ----
print(mean([1, 2, 3, 4, 4]))
print(mean([1, 2, 3, 4]))
print(mean([1, 2, 3]))
print(mean([10]))
print(mean([-1.0, 2.5, 3.25, 5.75]))
print(mean([0.1] * 10))
print(mean([1, 2.5]))
print(mean(range(1, 101)))
print(mean((3, 3, 3)))
print(mean(x * x for x in range(5)))
print(mean([True, False, True, True]))
print(mean([1e300, 3e300]), mean([1e-300, 3e-300]))
print(mean([-5, 5]), mean([7, 8]), mean([-7, -8]))
print(mean([0.5, 0.25, 0.125]), mean([2.5, 3.5, 10.0]), mean([1.5, 2.5, 3.5, 4.5]))
print(type(mean([1, 2, 3])).__name__, type(mean([1, 2])).__name__, type(mean([1.0, 2.0, 3.0])).__name__)
attempt("mean empty", mean, [])
attempt("mean text", mean, ["a", "b"])

# ---- fmean ----
print(fmean([1, 2, 3, 4]))
print(fmean([3.5, 4.0, 5.25]))
print(fmean([1, 2, 3]))
print(fmean([0.1] * 10))
print(fmean(range(10)))
print(fmean([1e16, 1.0, -1e16]))
print(type(fmean([2, 2])).__name__)
attempt("fmean empty", fmean, [])

# ---- median ----
print(median([1, 3, 5]))
print(median([1, 3, 5, 7]))
print(median([5, 1, 3]))
print(median([7]))
print(median([1, 2]))
print(median([1.5, 2.5, 10.0]))
print(median([3, 1, 2, 4, 5, 6]))
print(median(["b", "a", "c"]))
print(median(range(10)), median(range(11)))
print(median_low([1, 3, 5]), median_low([1, 3, 5, 7]), median_low([4]), median_low([2, 1]))
print(median_high([1, 3, 5]), median_high([1, 3, 5, 7]), median_high([4]), median_high([2, 1]))
print(median_low(["x", "y", "a", "b"]), median_high(["x", "y", "a", "b"]))
attempt("median empty", median, [])
attempt("median_low empty", median_low, [])
attempt("median_high empty", median_high, [])

# ---- mode ----
print(mode([1, 1, 2, 3, 3, 3, 3, 4]))
print(mode(["red", "blue", "blue", "red", "green", "red", "red"]))
print(mode([1, 2, 2, 1]))
print(mode([5]))
print(mode("aabbbc"))
print(mode([1.5, 1.5, 2]), mode([(1, 2), (1, 2), (3,)]))
print(multimode("aabbbbccddddeeffffgg"))
print(multimode([1, 2, 3]))
print(multimode([]))
print(multimode([1, 1, 2, 2, 3]))
print(multimode("mississippi"))
attempt("mode empty", mode, [])

# ---- variance and standard deviation ----
data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
print(variance(data))
print(stdev(data))
print(pvariance(data))
print(pstdev(data))
print(variance([1, 2, 3, 4, 5]), pvariance([1, 2, 3, 4, 5]))
print(variance([1, 2, 3, 4]), pvariance([1, 2, 3, 4]))
print(variance([2, 4, 4, 4, 5, 5, 7, 9]), pvariance([2, 4, 4, 4, 5, 5, 7, 9]))
print(stdev([2, 4, 4, 4, 5, 5, 7, 9]), pstdev([2, 4, 4, 4, 5, 5, 7, 9]))
print(variance([1, 1, 1, 1]), pvariance([1, 1, 1, 1]), stdev([3, 3]), pstdev([3]))
print(variance([1.0, 2.0, 3.0, 4.0]), pvariance([1.0, 2.0, 3.0, 4.0]))
print(variance([0.5, 1.5]), stdev([0.5, 1.5]), pvariance([0.5, 1.5]), pstdev([0.5, 1.5]))
print(variance([10, 20]), stdev([10, 20]), variance([1, 3]), stdev([1, 3]))
print(variance([1, 2]), pvariance([1, 2]), pvariance([7]), pvariance([1.5]))
print(variance(range(1, 11)), pvariance(range(1, 11)), stdev(range(1, 11)), pstdev(range(1, 11)))
print(variance([1.5, 2.5, 2.5, 2.75, 3.25, 4.75]), stdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75]))
print(pvariance([0.0, 0.25, 0.25, 1.25, 1.5, 1.75, 2.75, 3.25]), pstdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75]))
print(variance([100, 200, 300]), variance([-2, -1, 0, 1, 2]), pvariance([-2, -1, 0, 1, 2]))
print(variance([1, 2, 4]), variance([1, 2, 3, 5]), pvariance([1, 2, 4]))
print(variance([1, 2.0, 3]), variance([True, False, True]))
m = mean(data)
print(variance(data, m), pvariance(data, m), stdev(data, m), pstdev(data, m))
print(variance([1, 2, 3, 4], 2), pvariance([1, 2, 3, 4], 2), variance([1, 2, 3, 4], 2.5), pvariance([1, 2, 3], 2))
print(round(stdev([1, 2, 3, 4, 5]), 10), round(pstdev([1, 2, 3, 4, 5]), 10))
print(type(variance([1, 2, 3])).__name__, type(variance([1, 2])).__name__, type(pvariance([1, 3])).__name__)
attempt("variance one", variance, [1])
attempt("variance empty", variance, [])
attempt("stdev one", stdev, [1])
attempt("pvariance empty", pvariance, [])
attempt("pstdev empty", pstdev, [])
attempt("variance text", variance, ["a", "b"])

# ---- a little report ----
scores = {"ann": [82, 91, 77], "bob": [65, 70, 88, 92], "cy": [100]}
for name in scores:
    values = scores[name]
    print(name, mean(values), median(values), round(pstdev(values), 3), max(values) - min(values))
everything = [v for values in scores.values() for v in values]
print(mean(everything), median(everything), mode(everything), round(stdev(everything), 4))
print(issubclass(StatisticsError, ValueError), statistics.mean is mean)
try:
    mean([])
except ValueError as e:
    print("caught as ValueError:", e)
