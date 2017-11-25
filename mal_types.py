class MalType(object):
    value = "<MalType>"

    def __repr__(self):
        return repr(self.value)


class MalList(MalType, list):
    def __init__(self, p_type, *args, **kwargs):
        self.p_type = p_type
        super(MalList).__init__(*args, **kwargs)
    pass


class MalNumber(MalType):
    def __init__(self, value):
        self.value = int(value)


    def to_str(self):
        return str(self.value)


class MalSymbol(MalType):
    def __init__(self, value):
        self.value = str(value)

