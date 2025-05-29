import time


class A:
    def __init__(self):
        print("A的初始化方法被调用")
    def show(self):
        print("A的方法被调用")
class B(A):
    def __init__(self):
        # noinspection PyMissingConstructor
        super().show()  # 显式调用父类的__init__
        print("B的初始化方法被调用")
    def show(self):
        super().show()  # 显式调用父类的__init__
        print("B的方法被调用")

b = B()  # 输出: A的初始化方法被调用 → B的初始化方法被调用
time.sleep(1)
B().show()