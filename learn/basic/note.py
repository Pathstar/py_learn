
# 3.7后 dict遍历顺序就是插入顺序


class Animal:
    pass

class Dog(Animal):
    pass

def type():
    d = Dog()
    print(isinstance(d, Animal))  # True，Dog继承了Animal，isinstance返回真
    print(type(d) == Animal)  # False（因为实际上 type(d) 得到 Dog）



d = Dog()
print(f"isinstance {isinstance(d, Animal)}")  # True，Dog继承了Animal，isinstance返回真
print(type(d) == Animal)  # False（因为实际上 type(d) 得到 Dog）