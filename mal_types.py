class MalType(object):
    value = "<MalType>"

    def __str__(self):
        return str(self.value)


class MalList(MalType, list):
    def __init__(self, p_type, seq=None):
        if not seq:
            seq = ()
        super(MalList, self).__init__(seq)
        self.p_type = p_type


class MalNumber(MalType):
    def __init__(self, value):
        self.value = int(value)

    def to_str(self):
        return str(self.value)


class MalSymbol(MalType):
    def __init__(self, value):
        self.value = str(value)


class MalString(MalType):
    def __init__(self, value):
        self.value = str(value)


class MalKeyword(MalType):
    def __init__(self, value):
        self.value = str(value)


class MalNil(MalType, None):
    def __str__(self):
        return 'nil'


class MalBool(MalType, bool):
    def __str__(self):
        return ''

class MalException(Exception):
    pass

