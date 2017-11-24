def READ():
    return input("user> ")

def EVAL(arg):
    return arg

def PRINT(arg):
    print(arg)
    return arg

def rep():
    while True:
        PRINT(EVAL(READ()))

if __name__ == '__main__':
    rep()