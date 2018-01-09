from printer import pr_str
from reader import read_str
import mal_types


def prn(*args):
    print(" ".join([pr_str(i, print_readably=True) for i in args]))
    return mal_types.MalNil()

def println(*args):
    print(" ".join([pr_str(i, print_readably=False) for i in args]))
    return mal_types.MalNil()


def read_string(string):
    if isinstance(string, mal_types.MalString):
        string = string.data
    return read_str(string)

def slurp(filename):
    if isinstance(filename, mal_types.MalString):
        filename = filename.data
    with open(filename, 'rt') as f:
        file_content = f.read()  # break step 6 read text test, but seems no effect
    return mal_types.MalString(file_content)

def atom(obj):
    rv = mal_types.MalAtom(ref=obj)
    return rv

def is_atom(obj):
    return mal_types.MalBool(isinstance(obj, mal_types.MalAtom))

def deref(obj):
    return obj.ref

def reset(atom, value):
    atom.ref = value
    return atom.ref

def swap(atom, func, *args):
    atom.ref = func(atom.ref, *args)
    return atom.ref

def cons(obj, lst):
    rv = mal_types.MalList([obj])
    rv.data.extend(lst.data)
    return rv

def concat(*lsts):
    rv = mal_types.MalList()
    for l in lsts:
        rv.data.extend(l)
    return rv

def equal(a, b):
    if isinstance(a, mal_types.list_types) and isinstance(b, mal_types.list_types):
        if len(a) != len(b):
            return mal_types.MalBool(False)
        for x, y in zip(a, b):
            if not equal(x, y):
                return mal_types.MalBool(False)
        return mal_types.MalBool(True)
    if type(a) != type(b):
        return mal_types.MalBool(False)
    return mal_types.MalBool(a.data==b.data)

def is_list(x):
    if isinstance(x, mal_types.MalList):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def nth(lst, n):
    if isinstance(n, mal_types.MalNumber):
        n = n.data
    try:
        return lst[n]
    except IndexError:
        raise mal_types.MalException("index error")


def first(lst):
    if isinstance(lst, mal_types.MalNil) or len(lst) == 0:
        return mal_types.MalNil()
    return lst[0]

def rest(lst):
    if isinstance(lst, mal_types.MalNil):
        return mal_types.MalList()
    return mal_types.MalList(lst[1:])


ns = {
    '+': lambda a, b: mal_types.MalNumber(a.data + b.data), # fixme: operate and return maltypes directly
    '-': lambda a, b: mal_types.MalNumber(a.data - b.data),
    '*': lambda a, b: mal_types.MalNumber(a.data * b.data),
    '/': lambda a, b: mal_types.MalNumber((a.data / b.data)),

    "list": lambda *x: mal_types.MalList(list(x)),
    "list?": is_list,
    "empty?": lambda x: mal_types.MalBool(len(x) == 0),
    "count": lambda x: mal_types.MalNumber(len(x)),
    "=": equal,
    "<": lambda x, y: mal_types.MalBool(x.data<y.data),
    "<=": lambda x,y: mal_types.MalBool(x.data<=y.data),
    ">": lambda x,y: mal_types.MalBool(x.data>y.data),
    ">=": lambda x,y: mal_types.MalBool(x.data>=y.data),
    "pr-str": lambda *args: mal_types.MalString(" ".join([pr_str(i, print_readably=True) for i in args])),
    "str": lambda *args: mal_types.MalString("".join([pr_str(i, print_readably=False) for i in args])),
    "prn": prn,
    "println": println,


    "read-string": read_string,
    "slurp": slurp,

    "atom": atom,
    "atom?": is_atom,
    "deref": deref,
    "reset!": reset,
    "swap!": swap,

    "cons": cons,
    "concat": concat,

    "nth": nth,
    "first": first,
    "rest": rest,
}