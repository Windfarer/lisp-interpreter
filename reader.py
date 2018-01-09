import re
import mal_types

_mal_token_pattern = re.compile(r'''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)''')

_list_token_mapping = {
    '(': ')',
    '[': ']',
}

_list_ending_token = (')', ']')

_list_type_mapping = {
    '(': mal_types.MalList,
    '[': mal_types.MalVector,
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


def read_list(reader, starting_token):
    result = _list_type_mapping[starting_token]()
    reader.next()
    while True:
        token = read_form(reader)
        if token in _list_ending_token and token != _list_token_mapping[starting_token]:
            raise mal_types.MalException("expected '{}', got {}".format(_list_token_mapping[starting_token], token))
        if token is None:
            raise mal_types.MalException("expected 'EOF', got {}".format(token))
        if token in _list_ending_token:
            break
        result.append(token)
        reader.next()
    return result


def read_hash_map(reader):
    result = mal_types.MalHashMap()
    reader.next()
    while True:
        token = read_form(reader)
        if token in _list_ending_token:
            raise mal_types.MalException("expected '}', got {}".format(token))
        if token is None:
            raise mal_types.MalException("expected 'EOF', got {}".format(token))
        if token == '}':
            break
        key = token
        reader.next()
        token = read_form(reader)
        if token in _list_ending_token:
            raise mal_types.MalException("expected '}', got {}".format(token))
        if token is None:
            raise mal_types.MalException("expected 'EOF', got {}".format(token))
        if token == '}':
            break
        value = token
        reader.next()
        result[key] = value
    return result


def read_atom(reader):
    token = reader.peek()
    try:
        val = int(token)
        return mal_types.MalNumber(val)
    except ValueError:
        pass
    if token in _quote_mapping:
        reader.next()
        return mal_types.MalList([mal_types.MalSymbol(_quote_mapping[token]), read_form(reader)])
    elif token == '^':
        reader.next()
        meta_data = read_form(reader)
        reader.next()
        lst = read_form(reader)
        return mal_types.MalList(["with-meta", lst, meta_data])
    elif token.startswith('"') and token.endswith('"'):
        return mal_types.MalString(bytes(token[1:-1], "utf-8").decode("unicode_escape"))
    elif token.startswith(":"):
        return mal_types.MalKeyword(token)
    elif token in ('true', 'false'):
        if token == 'true':
            return mal_types.MalBool(True)
        return mal_types.MalBool(False)
    elif token == 'nil':
        return mal_types.MalNil()
    return mal_types.MalSymbol(token)  # symbol?


def read_form(reader):
    token = reader.peek()
    # print('-',  type(token), token)
    if not token:  # "EOF" or None
        return token
    if token in _list_token_mapping:
        return read_list(reader, token)
    if token == '{':
        return read_hash_map(reader)
    elif token in _list_ending_token:
        return token
    elif token == '}':
        return '}'
    return read_atom(reader)


def tokenizer(string):
    tokens = _mal_token_pattern.findall(string)
    return tokens


def read_str(string):
    tokens = tokenizer(string)
    # print("tokens", tokens)
    reader = Reader(tokens)
    return read_form(reader)


if __name__ == '__main__':
    print(tokenizer("(+ 2 (* 3 4) )"))
