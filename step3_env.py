import reader
import printer
import mal_types
from env import Env


def READ(string):
    return reader.read_str(string)


def EVAL(ast, env):
    if not isinstance(ast, mal_types.MalList):
        return eval_ast(ast, env)
    elif not ast:
        return ast
    elif isinstance(ast, mal_types.MalList):   # apply
        evaluated_ast = eval_ast(ast, env)
        if isinstance(evaluated_ast[0], mal_types.MalSymbol) and evaluated_ast[0].value == 'def!':
            env.set(evaluated_ast[1], evaluated_ast[2])
        elif isinstance(evaluated_ast[0], mal_types.MalSymbol) and evaluated_ast[0].value == 'let*':
            env.set(evaluated_ast[1], evaluated_ast[2])
        elif callable(evaluated_ast[0]):
            return evaluated_ast[0](*evaluated_ast[1:])
        return evaluated_ast
    return ast.value


def eval_ast(ast, env):
    if isinstance(ast, mal_types.MalSymbol):
        fn = env.get(ast.value)
        if not fn:
            raise mal_types.MalException("'{}' not found.".format(ast.value))
        return fn
    elif isinstance(ast, mal_types.MalList):
        return mal_types.MalList(ast.p_type, seq=[EVAL(i, env) for i in ast])
    return ast.value


def PRINT(ast):
    return printer.pr_str(ast)


repl_env = Env()
repl_env.set('+', lambda a,b: a+b)
repl_env.set('-', lambda a,b: a-b)
repl_env.set('*', lambda a,b: a*b)
repl_env.set('/', lambda a,b: int(a/b))


def rep():
    while True:
        try:
            print(PRINT(EVAL(READ(input("user> ")), repl_env)))
        except mal_types.MalException as e:
            print(e)


if __name__ == '__main__':
    rep()