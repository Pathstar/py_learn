class First(Exception):
    pass

class Two(First):
    pass

class Three(Two):
    pass

for cls in [First, Two, Three]:
    try:
        raise cls()
    except First:
        print("D")
    except Two:
        print("C")
    except Three:
        print("B")