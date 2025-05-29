class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person: {self.name}"

    def __repr__(self):
        return f"Person('{self.name}')"


p = Person("Bob")
print(p)  # 输出：Person: Bob（调用 __str__）
print(repr(p))  # 输出：Person('Bob')（调用 __repr__）
