import reader
import printer
import mal_types


def READ(string):
    return reader.read_str(string)


def EVAL(ast, env):
    if not isinstance(ast, mal_types.list_types):
        return eval_ast(ast, env)
    elif not ast:
        return ast
    elif isinstance(ast, mal_types.list_types):
        ast = eval_ast(ast, env)
        if len(ast) > 0 and callable(ast[0]):
            return ast[0](*ast[1:])
    return ast


def eval_ast(ast, env):
    if isinstance(ast, mal_types.MalSymbol):
        fn = env.get(ast.data)
        if not fn:
            raise mal_types.MalException("'{}' not found.".format(ast.data))
        return fn
    elif isinstance(ast, mal_types.list_types):
        class_type = ast.__class__
        return class_type([EVAL(i, env) for i in ast])
    elif isinstance(ast, mal_types.MalHashMap):
        return mal_types.MalHashMap({EVAL(k, env): EVAL(v, env) for k, v in ast.items()})
    return ast


def PRINT(ast):
    return printer.pr_str(ast)


repl_env = {
    '+': lambda a, b: mal_types.MalNumber(a.data + b.data), # fixme: operate and return maltypes directly
    '-': lambda a, b: mal_types.MalNumber(a.data - b.data),
    '*': lambda a, b: mal_types.MalNumber(a.data * b.data),
    '/': lambda a, b: mal_types.MalNumber((a.data / b.data)),
}


def rep():
    while True:
        try:
            print(PRINT(EVAL(READ(input("user> ")), repl_env)))
        except mal_types.MalException as e:
            print(e)
        except Exception as e:
            raise e
            print(e)


if __name__ == '__main__':
    rep()