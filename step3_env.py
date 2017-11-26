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
    elif isinstance(ast, mal_types.MalList):
        if isinstance(ast[0], mal_types.MalSymbol) and ast[0].value == 'def!':
            value = EVAL(ast[2], env)
            env.set(ast[1].value, value)
            return value
        elif isinstance(ast[0], mal_types.MalSymbol) and ast[0].value == 'let*':
            let_env = Env(outer=env)
            for k ,v in  zip(ast[1][::2], ast[1][1::2]):
                let_env.set(k.value, EVAL(v, let_env))
            return EVAL(ast[2], let_env)
        evaluated_ast = eval_ast(ast, env)
        if callable(evaluated_ast[0]):
            return evaluated_ast[0](*evaluated_ast[1:])  # apply
        return evaluated_ast
    return ast


def eval_ast(ast, env):
    if isinstance(ast, mal_types.MalSymbol):
        v = env.get(ast.value)
        if not v:
            raise mal_types.MalException("'{}' not found.".format(ast.value))
        return v
    elif isinstance(ast, mal_types.MalList):
        return mal_types.MalList(ast.p_type, seq=[EVAL(i, env) for i in ast])
    return ast.value


def PRINT(ast):
    return printer.pr_str(ast)


def rep():
    repl_env = Env()
    repl_env.set('+', lambda a, b: a + b)
    repl_env.set('-', lambda a, b: a - b)
    repl_env.set('*', lambda a, b: a * b)
    repl_env.set('/', lambda a, b: int(a / b))

    while True:
        try:
            print(PRINT(EVAL(READ(input("user> ")), repl_env)))
        except mal_types.MalException as e:
            print(e)


if __name__ == '__main__':
    rep()