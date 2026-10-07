# A module imported by modules.py.
CONSTANT = "from helper"

def double(n):
    return n * 2

def triple(n):
    return n * 3

class Shape:
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

if __name__ == "__main__":
    print("helper run directly")
