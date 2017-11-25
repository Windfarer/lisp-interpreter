from mal_types import MalType, MalSymbol, MalNumber, MalList


def pr_str(obj):
    if isinstance(obj, MalSymbol):
        return str(obj.value)
    elif isinstance(obj, MalNumber):
        return str(obj.value)
    elif isinstance(obj, MalList):
        return "({})".format(" ".join([pr_str(i) for i in obj]))