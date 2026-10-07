# Classes, exceptions and a little report.
class InsufficientFunds(Exception):
    def __init__(self, needed, available):
        super().__init__(f"need {needed:.2f}, have {available:.2f}")
        self.shortfall = needed - available


class Account:
    interest = 0.02

    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("a deposit must be more than nothing")
        self.balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds(amount, self.balance)
        self.balance -= amount
        self.history.append(("withdraw", amount))

    def __str__(self):
        return f"{self.owner}: {self.balance:,.2f}"


class Savings(Account):
    interest = 0.05

    def add_interest(self):
        self.deposit(self.balance * self.interest)


accounts = [Account("Ana", 120), Savings("Ben", 1000)]
accounts[0].deposit(30.5)
accounts[1].add_interest()
for account, amount in zip(accounts, [500, 250]):
    try:
        account.withdraw(amount)
        print(f"{account.owner} took out {amount}")
    except InsufficientFunds as e:
        print(f"{account.owner} can't take out {amount}: {e} (short by {e.shortfall:.2f})")
for account in accounts:
    print(account, [kind for kind, _ in account.history])
print("total:", sum(a.balance for a in accounts))
