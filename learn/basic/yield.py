def testgen():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5
g = testgen()
for x in g:
    print(x)
    # print(next(g))
    

print("-----")
g = testgen()
while True:
    try:
        x = next(g)
    except StopIteration:
        break
    print(x)