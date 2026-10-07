# A small program of the usual kind: an inventory with a report.
class Item:
    def __init__(self, name, price, quantity=1, tags=()):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.tags = set(tags)

    @property
    def total(self):
        return self.price * self.quantity

    def __repr__(self):
        return f"Item({self.name!r}, {self.price}, {self.quantity})"


class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, item):
        if item.name in self._items:
            self._items[item.name].quantity += item.quantity
        else:
            self._items[item.name] = item
        return self

    def remove(self, name, quantity=1):
        item = self._items.get(name)
        if item is None:
            raise KeyError(f"no item called {name!r}")
        if quantity > item.quantity:
            raise ValueError(f"only {item.quantity} {name} left")
        item.quantity -= quantity
        if item.quantity == 0:
            del self._items[name]

    def __iter__(self):
        return iter(sorted(self._items.values(), key=lambda i: i.name))

    def __len__(self):
        return len(self._items)

    def total(self):
        return sum(item.total for item in self)

    def by_tag(self):
        groups = {}
        for item in self:
            for tag in sorted(item.tags) or ["untagged"]:
                groups.setdefault(tag, []).append(item.name)
        return groups


def report(inventory):
    lines = [f"{'Item':<12}{'Qty':>5}{'Price':>10}{'Total':>12}", "-" * 39]
    for item in inventory:
        lines.append(f"{item.name:<12}{item.quantity:>5}{item.price:>10.2f}{item.total:>12,.2f}")
    lines.append("-" * 39)
    lines.append(f"{'Total':<27}{inventory.total():>12,.2f}")
    return "\n".join(lines)


inv = Inventory()
inv.add(Item("widget", 2.5, 100, ["small", "metal"])).add(Item("gadget", 19.99, 12, ["electronic"]))
inv.add(Item("gizmo", 1249.0, 3)).add(Item("widget", 2.5, 50))
print(report(inv))
print(len(inv), inv.by_tag())
for name, quantity in [("gadget", 2), ("gizmo", 5), ("thing", 1), ("gizmo", 3)]:
    try:
        inv.remove(name, quantity)
        print(f"removed {quantity} {name}")
    except (KeyError, ValueError) as e:
        print(f"{type(e).__name__}: {e}")
print(report(inv))

def primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for n in range(2, int(limit ** 0.5) + 1):
        if sieve[n]:
            for multiple in range(n * n, limit + 1, n):
                sieve[multiple] = False
    return [n for n, is_prime in enumerate(sieve) if is_prime]

print(primes(60), len(primes(10000)))

def word_frequencies(text):
    counts = {}
    for word in text.lower().split():
        word = word.strip(".,;!?")
        if word:
            counts[word] = counts.get(word, 0) + 1
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:5]

print(word_frequencies("The cat and the hat. The cat sat; the hat fell! And that was that."))

def hanoi(n, source="A", target="C", spare="B", moves=None):
    if moves is None:
        moves = []
    if n:
        hanoi(n - 1, source, spare, target, moves)
        moves.append((source, target))
        hanoi(n - 1, spare, target, source, moves)
    return moves

print(len(hanoi(10)), hanoi(2))
matrix = [[1, 2, 3], [4, 5, 6]]
transposed = [list(row) for row in zip(*matrix)]
print(transposed, [[sum(a * b for a, b in zip(r, c)) for c in zip(*transposed)] for r in matrix])
memo = {}
def collatz(n):
    if n == 1:
        return 1
    if n not in memo:
        memo[n] = 1 + collatz(n // 2 if n % 2 == 0 else 3 * n + 1)
    return memo[n]
print(max(range(1, 2000), key=collatz), collatz(27))
