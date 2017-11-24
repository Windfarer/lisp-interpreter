def READ():
    return input("user> ")

def EVAL(string):
    return string

def PRINT(string):
    print(string)

def rep():
    while True:
        PRINT(EVAL(READ()))

if __name__ == '__main__':
    rep()