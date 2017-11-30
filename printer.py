import mal_types

def pr_str(obj):
    if isinstance(obj, mal_types.MalString):
        return '"{}"'.format(obj)
    if isinstance(obj, mal_types.MalList):
        return '({})'.format(" ".join([pr_str(i) for i in obj]))
    elif isinstance(obj, mal_types.MalVector):
        return '[{}]'.format(" ".join([pr_str(i) for i in obj]))
    elif isinstance(obj, mal_types.MalVector):
        rv = []
        for k, v in obj:
            rv.append(k)
            rv.append(pr_str(v))
        return '{{}}'.format(" ".join(rv))
    else:
        return str(obj)