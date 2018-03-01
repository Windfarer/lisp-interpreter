from collections import OrderedDict
from itertools import chain


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

    def extend(self, lst):
        for i in lst:
            self.data.append(i)

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
        if isinstance(i, slice):
            return MalList(data=self.data.__getitem__(i))
        return self.data.__getitem__(i)

    def append(self, item):
        self.data.append(item)


class MalHashMap(MalType):
    def __init__(self, data=None):
        if not data:
            self.data = OrderedDict()
        elif isinstance(data, dict):
            self.data = OrderedDict(data)
        elif isinstance(data, MalHashMap):
            self.data = OrderedDict(data.data)
        elif isinstance(data, (MalList, MalVector, list)):
            self.data = OrderedDict()
            for k, v in zip(data[::2], data[1::2]):
                self.data[k] = v

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, key):
        return self.data.__getitem__(key)

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)

    def __delitem__(self, key):
        return self.data.__delitem__(key)

    def __len__(self):
        return len(self.data)

    def items(self):
        return self.data.items()

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return MalNil()

    def keys(self):
        return MalList(self.data.keys())

    def values(self):
        return MalList(self.data.values())

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

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        if not isinstance(other, MalString):
            return False
        return hash(self.data) == hash(other.data)

class MalKeyword(MalType):  # fixme: special unicode?
    def __init__(self, data):
        self.data = str(data)

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        if not isinstance(other, MalKeyword):
            return False
        return hash(self.data) == hash(other.data)


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
    def __repr__(self):
        return "<MalFn>"

    def __str__(self):
        return self.__repr__()

    def __init__(self, ast, params, env, fn):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = False

    def __call__(self, *args):
        return self.fn(*args)

class MalAtom(MalType):
    def __init__(self, ref):
        self.ref = ref

class MalException(Exception):
    def __init__(self, data):
        self.data = data

list_types = (MalList, MalVector)
