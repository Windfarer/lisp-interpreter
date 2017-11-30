class MalType(object):
    data = None

    def __str__(self):
        return str(self.data)


class MalList(MalType):
    def __init__(self, data=None):
        if not data:
            data = []
        if isinstance(data, MalList):
            data = data.data
        self.data = data

    def __iter__(self):
        pass # todo

    def __getitem__(self, i):
        return self.data.__getitem__(i)

    def append(self, item):
        self.data.append(item)


class MalVector(MalType):
    def __init__(self, data=None):
        if not data:
            data = []
        if isinstance(data, MalVector):
            data = data.data
        self.data = data

    def __iter__(self):
        pass # todo

    def __getitem__(self, i):
        return self.data.__getitem__(i)

    def append(self, item):
        self.data.append(item)


class MalHashMap(MalType):
    def __init__(self, data=None):
        if not data:
            data = {}
        if isinstance(data, MalHashMap):
            data = data.data
        self.data = data

    def __iter__(self):
        pass # todo

    def __getitem__(self, key):
        return self.data.__getitem__(key)


class MalNumber(MalType):
    def __init__(self, data):
        self.data = int(data)

    def to_str(self):
        return str(self.data)


class MalSymbol(MalType):
    def __init__(self, data):
        self.data = str(data)


class MalString(MalType):
    def __init__(self, data):
        self.data = str(data)


class MalKeyword(MalType):
    def __init__(self, data):
        self.data = str(data)


class MalBool(MalType):
    def __init__(self, data):
        self.data = bool(data)


class MalNil(MalType):
    def __init__(self, data):
        self.data = bool(data)


class MalException(Exception):
    pass

