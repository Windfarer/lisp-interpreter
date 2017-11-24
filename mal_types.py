class MalType(object):
    pass

class MalList(MalType, list):
    pass

class MalNumber(MalType):
    def __init__(self, value):
        self.value = int(value)

    def to_str(self):
        return str(self.value)


class MalSymbol(MalType):
    def __init__(self, value):
        self.value = str(value)