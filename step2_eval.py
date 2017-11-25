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
        rv = eval_ast(ast, env)
        return rv[0](*rv[1:])
    return ast.value


def eval_ast(ast, env):
    if isinstance(ast, mal_types.MalSymbol):
        # print(ast.value)
        fn = env.get(ast.value)
        if not fn:
            raise Exception("'{}' not found.".format(ast.value))
        return fn
    elif isinstance(ast, mal_types.MalList):
        return mal_types.MalList(ast.p_type, seq=[EVAL(i, env) for i in ast])
    return ast.value


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
        except Exception as e:
            print(e)


if __name__ == '__main__':
    rep()