import re
from mal_types import MalType, MalList, MalNumber, MalSymbol

_mal_token_pattern = re.compile('''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)''')

_p_mapping = {
    '(': ')',
    '[': ']',
    '{': '}'
}

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
    first_token = reader.peek()
    result = MalList(p_type=first_token+_p_mapping[first_token])
    reader.next()
    while True:
        token = read_form(reader)
        if token is None:
             break
        elif token is "":
            return "expected '{}', got EOF".format(result.p_type[1])
        result.append(token)
        reader.next()
    return result


def read_atom(token):
    if token.isdigit():
        return MalNumber(token)
    return MalSymbol(token)  # symbol?


def read_form(reader):
    token = reader.peek()
    if not token:
        return ""
    if token in _p_mapping.keys():
        return read_list(reader)
    elif token in _p_mapping.values():
        return None
    return read_atom(token)


def tokenizer(string):
    tokens = _mal_token_pattern.findall(string)
    return tokens


def read_str(string):
    tokens = tokenizer(string)
    # print(tokens)
    reader = Reader(tokens)
    return read_form(reader)


if __name__ == '__main__':
    print(tokenizer("(+ 2 (* 3 4) )"))
