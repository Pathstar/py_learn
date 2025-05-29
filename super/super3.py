import time

class AA:
    def show(self):
        print("AA")

class A:
    def show(self):
        print("A")

class B(AA):
    def show(self):
        print("B")
        time.sleep(1)
        super().show()

class C(A):
    def show(self):
        print("C")
        # time.sleep(1)
        super().show()
        # super(C, self).show()
# class D(B, C): pass
# class D(B, C):
# ↑ 结果一致
class D(B):
    def show(self):
        print("D")
        time.sleep(1)
        super().show()

#         B(C) C(A) 不是B(AA) C(A)不会抢占B(AA)的super super为(AA)
# 如果 C(A) B(A) 都是A，B的super指到C中

d = D()
D().show()  # 输出：D → B → C → A
print(D.__mro__)  # 查看 MRO 顺序：D → B → C → A → object