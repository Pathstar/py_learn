class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)  # 调用父类的 __init__
        self.age = age

child = Child("Alice", 10)
print(child.name)  # 输出：Alice
