import time


class Adder:
    def __init__(self, base):
        self.base = base
        print(f"init {base}")

    def __call__(self, x):
        print(f"call {x}")
        return self.base + x
# self = 5
# add5 = 5 -> self = 5
add5 = Adder(5)
time.sleep(1)
print(add5(3))
