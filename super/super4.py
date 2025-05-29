class A:
    def __init__(self):
        print("A的初始化方法被调用")
class B(A):
    def __init__(self):
        super().__init__()  # 显式调用父类的__init__
        print("B的初始化方法被调用")
b = B()  # 输出: A的初始化方法被调用 → B的初始化方法被调用