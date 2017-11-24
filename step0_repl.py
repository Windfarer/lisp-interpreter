def READ(string):
    return string


def EVAL(string):
    return string


def PRINT(string):
    return string


def rep():
    while True:
        print(PRINT(EVAL(READ(input("user> ")))))


if __name__ == '__main__':
    rep()