from collections import OrderedDict

class MalType(object):
    data = None

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, repr(self.data))

    def __str__(self):
        return str(self.data)

    def __bool__(self):
        return True

    def __len__(self):
        return len(self.data)

    def __le__(self, other):
        return self.data.__le__(other.data)

    def __lt__(self, other):
        return self.data.__lt__(other.data)


class MalList(MalType):
    def __init__(self, data=None):
        if not data:
            data = []
        if isinstance(data, MalList):
            data = data.data
        self.data = list(data)

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, i):
        if isinstance(i, slice):
            return MalList(data=self.data.__getitem__(i))
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
        return self.data.__iter__()

    def __getitem__(self, i):
        return self.data.__getitem__(i)

    def append(self, item):
        self.data.append(item)


class MalHashMap(MalType):
    def __init__(self, data=None):
        if not data:
            data = OrderedDict()
        if isinstance(data, MalHashMap):
            data = data.data
        self.data = OrderedDict(data)

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, key):
        return self.data.__getitem__(key)

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)

    def items(self):
        return self.data.items()

class MalNumber(MalType):
    def __init__(self, data):
        self.data = int(data)

    def to_str(self):
        return str(self.data)

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        if isinstance(other, MalType):
            return self.data == other.data
        return self.data == other


class MalSymbol(MalType):
    def __init__(self, data):
        self.data = str(data)

    def __hash__(self):
        return hash(self.data)

class MalString(MalType):
    def __init__(self, data):
        self.data = str(data)

class MalKeyword(MalType):
    def __init__(self, data):
        self.data = str(data)


class MalBool(MalType):
    def __init__(self, data):
        if isinstance(data, bool):
            self.data = data
        else:
            self.data = bool(data)

    def __str__(self):
        return 'true' if self.data else 'false'

    def __bool__(self):
        return self.data


class MalNil(MalType):
    def __init__(self):
        self.data = None

    def __str__(self):
        return 'nil'

    def __bool__(self):
        return False

    def __len__(self):
        return 0

class MalFn(MalType):
    def __init__(self, ast, params, env, fn):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = False

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

class MalAtom(MalType):
    def __init__(self, ref):
        self.ref = ref

class MalException(Exception):
    pass

