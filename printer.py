import mal_types

def pr_str(obj, print_readably=True):
    if isinstance(obj, mal_types.MalString):
        return '"{}"'.format(obj)
    if callable(obj):
        return '#<function>'
    if isinstance(obj, mal_types.MalList):
        return '({})'.format(" ".join([pr_str(i) for i in obj]))
    elif isinstance(obj, mal_types.MalVector):
        return '[{}]'.format(" ".join([pr_str(i) for i in obj]))
    elif isinstance(obj, mal_types.MalHashMap):
        rv = []
        for k, v in obj:
            rv.append(k)
            rv.append(pr_str(v))
        return '{{}}'.format(" ".join(rv))
    else:
        return str(obj)