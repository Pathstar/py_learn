def fibs():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a+b

gen = fibs()
for i, n in enumerate(gen):
    if i > 100: break
    print(n)
    #
    # 举一个必须用生成器的“无限序列”例子
    # 比如你需要产生无限斐波那契数列：
    # 这里如果你用列表[a, b, ...]
    # 来装，那你永远都装不完，也根本用不了
    # 生成器可以无限“产出”下一个，而不用提前占用无限内存

def fibs2():
    a = 0      # 斐波那契数列第一项
    b = 1      # 第二项
    while True:
        yield a    # 返回当前a，并暂停
        temp = a + b
        a = b
        b = temp

        # 或者 a, b = b, a + b 语法糖

gen = fibs2()
i = 0
while True:
    n = next(gen)    # 获取下一个斐波那契数
    if i > 100:     # 若已取超过1000项就退出
        break
    print(n)
    i += 1
