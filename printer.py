import mal_types

def pr_str(obj, print_readably=True):
    if isinstance(obj, mal_types.MalString):
        if print_readably is False:
            return str(obj)
        rv = '"{}"'.format(obj)
    elif callable(obj):
        rv = '#<function>'
    elif isinstance(obj, mal_types.MalAtom):
        rv = "(atom {})".format(pr_str(obj.ref))
    elif isinstance(obj, mal_types.MalList):
        rv = '({})'.format(" ".join([pr_str(i) for i in obj]))
    elif isinstance(obj, mal_types.MalKeyword):
        rv = obj.data
    elif isinstance(obj, mal_types.MalVector):
        rv = '[{}]'.format(" ".join([pr_str(i) for i in obj]))
    elif isinstance(obj, mal_types.MalHashMap):
        l = []
        for k, v in obj.items():
            l.append(pr_str(k))
            l.append(pr_str(v))
        # print(l)
        rv = '{%s}' % " ".join(l)
    else:
        rv = str(obj)
    return rv
    # if print_readably:
    #     return rv
    # else:
    #     return repr(rv)[1:-1]