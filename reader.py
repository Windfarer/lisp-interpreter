import re
import mal_types

_mal_token_pattern = re.compile(r'''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)''')

_p_mapping = {
    '(': ')',
    '[': ']',
    '{': '}'
}

_quote_mapping = {
    "'": "quote",
    "`": "quasiquote",
    "~": "unquote",
    "~@": "splice-unquote",
    "@": "deref"
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
    result = mal_types.MalList()
    error = False
    reader.next()
    while True:
        token = read_form(reader)
        if token in _p_mapping.values() and token != result.p_type[1]:
            error = True
            break
        if token is None:
            error = True
            break
        if token in _p_mapping.values():
            break
        result.append(token)
        # print(token)
        reader.next()
    if error:
        if token is None:
            token = 'EOF'
        raise mal_types.MalException("expected '{}', got {}".format(result.p_type[1], token))
    return result


def read_atom(reader):
    token = reader.peek()
    # print(token)
    try:
        val = int(token)
        return mal_types.MalNumber(val)
    except ValueError:
        pass
    if token in _quote_mapping:
        reader.next()
        return mal_types.MalList([_quote_mapping[token], read_form(reader)])
    if token == '^':
        reader.next()
        meta_data = read_form(reader)
        reader.next()
        lst = read_form(reader)
        return mal_types.MalList(["with-meta", lst, meta_data])
    if token.startswith('"') and token.endswith('"'):
        return mal_types.MalString(token)
    if token.startswith(":"):
        return mal_types.MalKeyword(token)
    return mal_types.MalSymbol(token)  # symbol?


def read_form(reader):
    token = reader.peek()
    # print('-', token)
    if not token:  # "EOF" or None
        return token
    if token in _p_mapping:
        return read_list(reader)
    elif token in _p_mapping.values():
        return token
    return read_atom(reader)


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
