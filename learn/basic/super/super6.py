import time

class AA:
    def show(self):
        print("AA")

class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")
        time.sleep(1)
        super().show()

class C(B):
    def show(self):
        print("C")
        # time.sleep(1)
        super().show()

# class D(B, C): pass
class D(C, ):
    def show(self):
        print("D")
        time.sleep(1)
        super().show()

class E(D):
    def show(self):
        print("E")
        time.sleep(1)
        super().show()

d = D()
E().show()  # 输出：D → B → C → A
print(D.__mro__)  # 查看 MRO 顺序：D → B → C → A → object
# d->(b->a,c->a)



# 定义了四个类：A、B、C、D。其中，D继承自B和C，B和C都继承自A。每个类都有一个show方法，其中B、C、D的show方法都调用了super().show()。用户创建了D的实例并调用show()，结果输出顺序是D→B→C→A，但用户认为A会被触发两次，这可能是因为对MRO（方法解析顺序）和super()的工作原理不太清楚。
#
# 首先，我需要确定D的MRO。Python使用C3线性化算法来确定继承顺序。对于类D(B, C)，其MRO应该是D→B→C→A→object。可以使用D.__mro__来查看。这样，当调用super().show()时，会按照MRO顺序查找下一个类的方法。
#
# 在D的show方法中，调用super().show()，此时会找到B的show方法。B的show方法打印"B"，然后调用super().show()，此时按照MRO，下一个类是C，所以进入C的show方法。C的show方法打印"C"，调用super().show()，
