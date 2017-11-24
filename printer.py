from mal_types import MalType, MalSymbol, MalNumber, MalList


def pr_str(obj):
    if isinstance(obj, MalSymbol):
        return obj.value
    elif isinstance(obj, MalNumber):
        return obj.value
    elif isinstance(obj, MalList):
        return "("+ " ".join([pr_str(i) for i in obj]) + ")"