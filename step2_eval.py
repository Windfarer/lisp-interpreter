import reader
import printer
import mal_types


def READ(string):
    return reader.read_str(string)


def EVAL(ast, env):
    if not isinstance(ast, mal_types.MalList):
        return eval_ast(ast, env)
    elif not ast:
        return ast
    elif isinstance(ast, mal_types.MalList):
        ast = eval_ast(ast, env)
        if callable(ast[0]):
            return ast[0](*ast[1:])
        else:
            return ast
    return ast.data


def eval_ast(ast, env):
    if isinstance(ast, mal_types.MalSymbol):
        fn = env.get(ast.data)
        if not fn:
            raise mal_types.MalException("'{}' not found.".format(ast.data))
        return fn
    elif isinstance(ast, mal_types.MalList):
        return mal_types.MalList([EVAL(i, env) for i in ast])
    return ast.data


def PRINT(ast):
    return printer.pr_str(ast)


repl_env = {'+': lambda a,b: a+b,
            '-': lambda a,b: a-b,
            '*': lambda a,b: a*b,
            '/': lambda a,b: int(a/b)}


def rep():
    while True:
        try:
            print(PRINT(EVAL(READ(input("user> ")), repl_env)))
        except mal_types.MalException as e:
            print(e)


if __name__ == '__main__':
    rep()