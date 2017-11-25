import re
from mal_types import MalType, MalList, MalNumber, MalSymbol

_mal_token_pattern = re.compile('''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)''')


class Reader(object):
    def __init__(self, tokens=None):
        if tokens is None:
            self.tokens = []
        else:
            self.tokens = tokens
        self.position = 0

    def next(self):
        current_position = self.position
        if current_position >= len(self.tokens):
            return None
        self.position += 1
        return self.tokens[current_position]

    def peek(self):
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]


def read_list(reader):
    result = MalList()
    token = read_form(reader)
    while token is not None:
        result.append(token)
        token = read_form(reader)
    return result


def read_atom(token):
    if token.isdigit():
        return MalNumber(token)
    elif token.startswith('('):
        token = token[1:]
    return MalSymbol(token)  # symbol?


def read_form(reader):
    token = reader.next()
    if token[0] == '(':
        return read_list(reader)
    elif token == ')':
        return None
    return read_atom(token)


def tokenizer(string):
    tokens = _mal_token_pattern.findall(string)
    return tokens


def read_str(string):
    tokens = tokenizer(string)
    reader = Reader(tokens)
    return read_form(reader)


if __name__ == '__main__':
    print(tokenizer("(+ 2 (* 3 4) )"))
