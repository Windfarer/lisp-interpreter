from printer import pr_str
from reader import read_str
import mal_types
from time import time
import types
from copy import copy
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
        file_content = f.read()
    return mal_types.MalString(file_content)

def atom(obj):
    rv = mal_types.MalAtom(ref=obj)
    return rv

def is_atom(obj):
    return mal_types.MalBool(isinstance(obj, mal_types.MalAtom))

def deref(obj):
    if isinstance(obj, mal_types.MalAtom):
        return obj.ref
    return obj  # fixme?

def reset(atom, value):
    atom.ref = value
    return atom.ref

def swap(atom, func, *args):
    atom.ref = func(atom.ref, *args)
    return atom.ref

def cons(obj, lst):
    rv = mal_types.MalList([obj])
    if isinstance(lst, list):  #fixme
        rv.data.extend(lst)
    else:  #
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
    if isinstance(a, mal_types.MalHashMap) and isinstance(b, mal_types.MalHashMap):
        if len(a) != len(b):
            return mal_types.MalBool(False)
        # todo hashmap equal
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
        raise mal_types.MalException("nth: index out of range")


def first(x):
    if any([isinstance(x, mal_types.MalNil),
            isinstance(x, mal_types.list_types) and len(x) == 0,
           ]):
        return mal_types.MalNil()
    return x[0]

def rest(lst):
    if isinstance(lst, mal_types.MalNil):
        return mal_types.MalList()
    return mal_types.MalList(lst[1:])

def throw(x):
    raise mal_types.MalException(x)

def is_nil(x):
    if isinstance(x, mal_types.MalNil):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def is_true(x):
    if isinstance(x, mal_types.MalBool) and x.data is True:
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def is_false(x):
    if isinstance(x, mal_types.MalBool) and x.data is False:
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def symbol(x):
    return mal_types.MalSymbol(x.data)

def is_symbol(x):
    if isinstance(x, mal_types.MalSymbol):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def keyword(x):
    if isinstance(x, mal_types.MalString):
        return mal_types.MalKeyword(":{}".format(x.data))
    raise ValueError

def is_keyword(x):
    if isinstance(x, mal_types.MalKeyword):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def vector(*args):
    return mal_types.MalVector(args)

def is_vector(x):
    if isinstance(x, mal_types.MalVector):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def hash_map(*args):
    rv = mal_types.MalHashMap()
    for m, n in zip(args[::2], args[1::2]):
        rv[m] = n
    return rv

def is_hash_map(x):
    if isinstance(x, mal_types.MalHashMap):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def is_number(x):
    if isinstance(x, mal_types.MalNumber):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def is_string(x):
    if isinstance(x, mal_types.MalString):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def assoc(x, *args):
    rv = mal_types.MalHashMap(x)
    for m, n in zip(args[::2], args[1::2]):
        rv[m] = n
    return rv

def dissoc(x, *args):
    rv = mal_types.MalHashMap(x)
    for key in args:
        del[x[key]]
    return rv

def get(x, key):
    if isinstance(x, mal_types.MalHashMap):
        return x.get(key)
    return mal_types.MalNil()

def is_contains(x, key):
    if isinstance(x, mal_types.MalHashMap) and key in x:
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def keys(x):
    return x.keys()

def vals(x):
    return x.values()

def is_sequential(x):
    if isinstance(x, mal_types.list_types):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def apply(f, *args):
    lst = []
    lst.extend(args[:-1])
    lst.extend(args[-1])
    return f(*lst)

def map_(f, lst):
    return mal_types.MalList([f(i) for i in lst])

def readline(string):
    try:
        return mal_types.MalString(input(string))
    except EOFError:
        return mal_types.MalNil()

def meta(x):
    return getattr(x, 'metadata', mal_types.MalNil())

def with_meta(x, metadata):
    rv = copy(x)
    rv.metadata = metadata
    return rv

def conj(collection, *elements):
    if isinstance(collection, mal_types.MalList):
        lst = collection.data
        for i in elements:
            lst.insert(0, i)
        return mal_types.MalList(lst)
    if isinstance(collection, mal_types.MalVector):
        lst = collection.data
        for i in elements:
            lst.append(i)
        return mal_types.MalVector(lst)

def seq(x):
    if not x.data:
        return mal_types.MalNil()
    elif isinstance(x, mal_types.MalList):
        return x
    elif isinstance(x, mal_types.MalVector):
        return mal_types.MalList(x.data)
    elif isinstance(x, mal_types.MalString):
        return mal_types.MalList([mal_types.MalString(i) for i in x.data])

def is_function(x):
    if isinstance(x, mal_types.MalFn) or isinstance(x, types.FunctionType):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)

def is_macro(x):  #fixme
    if isinstance(x, mal_types.MalFn) or isinstance(x, types.FunctionType):
        return mal_types.MalBool(True)
    return mal_types.MalBool(False)


ns = {
    '+': lambda a, b: mal_types.MalNumber(a.data + b.data), # fixme: operate and return maltypes directly
    '-': lambda a, b: mal_types.MalNumber(a.data - b.data),
    '*': lambda a, b: mal_types.MalNumber(a.data * b.data),
    '/': lambda a, b: mal_types.MalNumber((a.data / b.data)),

    "list": lambda *x: mal_types.MalList(list(x)),
    "list?": is_list,
    "vector": vector,
    "vector?": is_vector,
    "hash-map": hash_map,
    "map?": is_hash_map,
    "assoc": assoc,
    "dissoc": dissoc,

    "get": get,
    "contains?": is_contains,
    "keys": keys,
    "vals": vals,
    "sequential?": is_sequential,
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

    "throw": throw,
    "nil?": is_nil,
    "true?": is_true,
    "false?": is_false,
    "symbol": symbol,
    "symbol?": is_symbol,
    "keyword": keyword,
    "keyword?": is_keyword,
    "number?": is_number,
    "string?": is_string,
    "fn?": is_function,
    "macro?": is_macro,

    "apply": apply,
    "map": map_,

    "readline": readline,

    "meta": meta,
    "with-meta": with_meta,

    "*host-language*": mal_types.MalString("python"),
    "time-ms": lambda : mal_types.MalNumber(int(time()*1000)),
    "conj": conj,
    "seq": seq
}