from printer import pr_str
import mal_types

ns = {
    '+': lambda a, b: mal_types.MalNumber(a.data + b.data), # fixme: add two maltype directly
    '-': lambda a, b: mal_types.MalNumber(a.data - b.data),
    '*': lambda a, b: mal_types.MalNumber(a.data * b.data),
    '/': lambda a, b: mal_types.MalNumber((a.data / b.data)),
    "prn": lambda x: pr_str(x, print_readably=True),
    "list": lambda *x: mal_types.MalList(x),
    "list?": lambda x: True if isinstance(x, list) else False,
    "empty?": lambda x: len(x) == 0,
    "count": lambda x: len(x),
    "=": lambda x,y: x==y,
    "<=": lambda x,y: x<=y,
    ">": lambda x,y: x>y,
    ">=": lambda x,y: x>=y,
}