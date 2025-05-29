# 1. 直接 for 循环
lst = [1, 2, 3, 4, 5]
for item in lst:
    print(item)
# 说明：最常用、最Pythonic，适合只用元素、不需要下标。

print("2-------------------------------------")
# 2. for + range() 按索引遍历
lst = [1, 2, 3, 4, 5]
for i in range(len(lst)):
    print(i, lst[i])
# 说明：需要用到下标（索引）时用此法。
print("3-------------------------------------")

# 3. for + enumerate() 同时取元素和下标
lst = [1, 2, 3, 4, 5]
for i, item in enumerate(lst):
    print(i, item)
# 说明：推荐！高效且直观，经常用于既要索引又要元素的场景。
print("4-------------------------------------")

# 4. while 循环
lst = [1, 2, 3, 4, 5]
i = 0
while i < len(lst):
    print(lst[i])
    i += 1
# 说明：不常用，适用于需要灵活控制流程、或在循环过程中动态变化下标的情况。
print("5-------------------------------------")

# 5. 列表推导式遍历（一般用于生成新列表/处理结果，不推荐只为遍历而用）
lst = [1, 2, 3, 4, 5]
squares = [x**2 for x in lst]
print(squares)
# 说明：适合需要“对每个元素产生一个新值”的批量操作。
print("6-------------------------------------")

# 6. map 或 filter 函数
lst = [1, 2, 3, 4, 5]
for x in map(str, lst): #将数字转换为字符串
    print(x)
# 说明：适合需要做元素转换、过滤等。
print("7-------------------------------------")

# 7. 反向遍历
lst = [1, 2, 3, 4, 5]
for item in reversed(lst):
    print(item)
# 说明：遍历顺序从后往前。
print("8-------------------------------------")

# 8. 遍历多个列表
a = [1, 2, 3]
b = ['a', 'b', 'c']
for x, y in zip(a, b):
    print(x, y)
# 说明：zip打包，适用于多个列表同时遍历。

print("9-------------------------------------")
lst = [1, 'hello', '', 'world']
for x in filter(None, lst):
    print(x)

# filter为
# for x in lst:
#     if bool(x):

# 在Python里，以下类型的值都是“假值”（bool(x) 为 False）：
# None
# False
# 0（包括整数0、浮点数0.0、复数0j等）
# 空字符串 ''
# 空列表 []
# 空元组 ()
# 空字典 {}
print("10-------------------------------------")
lst = [1, 'hello', '', 'world', None, 3.14, 'python']
for x in filter(lambda x: x is not None and x != '' and not isinstance(x, (int, float)), lst):
    print(x)