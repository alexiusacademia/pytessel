# Counts the words of a file (or of this program): python's usual first script.
#
#   pytessel examples/wordcount.py README.md
import sys

path = sys.argv[1] if len(sys.argv) > 1 else sys.argv[0]
counts = {}
with open(path) as f:
    for line in f:
        for word in line.lower().split():
            word = word.strip(".,:;!?()[]{}\"'`#*")
            if word.isalpha():
                counts[word] = counts.get(word, 0) + 1

print(f"{sum(counts.values())} words, {len(counts)} different, in {path}")
for word, count in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:10]:
    print(f"{word:<12} {count:>4} {'#' * count}")
