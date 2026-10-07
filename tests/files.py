# Reading and writing files.
import os
path = "adder_test_file.txt"
with open(path, "w") as f:
    f.write("first line\n")
    f.write("second line\n")
    print("third", "line", file=f)
with open(path) as f:
    print(repr(f.read()))
with open(path) as f:
    for number, line in enumerate(f, 1):
        print(number, line.rstrip())
f = open(path, "a")
f.write("appended\n")
f.close()
print(f.closed, open(path).readlines()[-1], len(open(path).read().splitlines()))
g = open(path)
print(repr(g.readline()), repr(g.readline()), [l.strip() for l in g])
g.close()
os.remove(path)
print(os.path.exists(path))
try:
    open("does/not/exist.txt")
except FileNotFoundError as e:
    print("FileNotFoundError:", e)
except OSError as e:
    print("other", e)
