import mal_types

def pr_str(obj, print_readably=True):
    if isinstance(obj, mal_types.MalString):
        rv = '"{}"'.format(obj)
    elif callable(obj):
        rv = '#<function>'
    elif isinstance(obj, mal_types.MalList):
        rv = '({})'.format(" ".join([pr_str(i) for i in obj]))
    elif isinstance(obj, mal_types.MalVector):
        rv = '[{}]'.format(" ".join([pr_str(i) for i in obj]))
    elif isinstance(obj, mal_types.MalHashMap):
        l = []
        for k, v in obj:
            l.append(k)
            l.append(pr_str(v))
        rv = '{{}}'.format(" ".join(l))
    else:
        rv = str(obj)
    if print_readably:
        return rv
    else:
        return repr(rv)[1:-1]