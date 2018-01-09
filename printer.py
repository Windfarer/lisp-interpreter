import mal_types

def pr_str(obj, print_readably=True):
    if isinstance(obj, mal_types.MalString):
        if print_readably is False:
            return obj.data
        return '"{}"'.format(obj.data.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n'))
    elif callable(obj):
        return '#<function>'
    elif isinstance(obj, mal_types.MalAtom):
        return "(atom {})".format(pr_str(obj.ref))
    elif isinstance(obj, mal_types.MalList):
        return '({})'.format(" ".join([pr_str(i, print_readably=print_readably) for i in obj]))
    elif isinstance(obj, mal_types.MalKeyword):
        return obj.data
    elif isinstance(obj, mal_types.MalVector):
        return '[{}]'.format(" ".join([pr_str(i, print_readably=print_readably) for i in obj]))
    elif isinstance(obj, mal_types.MalHashMap):
        l = []
        for k, v in obj.items():
            l.append(pr_str(k))
            l.append(pr_str(v))
        return '{%s}' % " ".join(l)
    return str(obj)
