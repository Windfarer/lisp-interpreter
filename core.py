from printer import pr_str
from reader import read_str
import mal_types


def prn(*args):
    print(" ".join([pr_str(i, print_readably=True) for i in args]))
    return mal_types.MalNil()

def read_string(string):
    if isinstance(string, mal_types.MalString):
        string = string.data
    return read_str(string)

def slurp(filename):
    if isinstance(filename, mal_types.MalString):
        filename = filename.data
    with open(filename, 'rt') as f:
        file_content = repr(f.read())[1:-1]
    return mal_types.MalString(file_content)

def atom():
    pass

def is_atom():
    pass

def deref():
    pass

def reset():
    pass

def swap():
    pass

def println(args):
    print(" ".join([pr_str(i, print_readably=False) for i in args]))
    return mal_types.MalNil()

ns = {
    '+': lambda a, b: mal_types.MalNumber(a.data + b.data), # fixme: operate and return maltypes directly
    '-': lambda a, b: mal_types.MalNumber(a.data - b.data),
    '*': lambda a, b: mal_types.MalNumber(a.data * b.data),
    '/': lambda a, b: mal_types.MalNumber((a.data / b.data)),

    "list": lambda *x: mal_types.MalList(x),
    "list?": lambda x: mal_types.MalBool(True if isinstance(x, mal_types.MalList) else False),
    "empty?": lambda x: mal_types.MalBool(len(x) == 0),
    "count": lambda x: mal_types.MalNumber(len(x)),
    "=": lambda x,y: mal_types.MalBool(x.data==y.data),
    "<": lambda x, y: mal_types.MalBool(x.data<y.data),
    "<=": lambda x,y: mal_types.MalBool(x.data<=y.data),
    ">": lambda x,y: mal_types.MalBool(x.data>y.data),
    ">=": lambda x,y: mal_types.MalBool(x.data>=y.data),
    "pr-str": lambda *args: " ".join([pr_str(i, print_readably=True) for i in args]),
    "str": lambda *args: " ".join([pr_str(i, print_readably=False) for i in args]),
    "prn": prn,
    "println": println,


    "read-string": read_string,
    "slurp": slurp,

    "atom": atom,
    "atom?": is_atom,
    "deref": deref,
    "reset!": reset,
    "swap!": swap,
}