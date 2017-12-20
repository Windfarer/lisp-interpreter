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
        if len(ast) == 0:
            return ast
        if isinstance(ast[0], mal_types.MalSymbol) and ast[0].data == 'def!':
            value = EVAL(ast[2], env)
            env.set(ast[1].data, value)
            return value
        elif isinstance(ast[0], mal_types.MalSymbol) and ast[0].data == 'let*':
            let_env = Env(outer=env)
            for k ,v in  zip(ast[1][::2], ast[1][1::2]):
                let_env.set(k.data, EVAL(v, let_env))
            return EVAL(ast[2], let_env)
        evaluated_ast = eval_ast(ast, env)
        if callable(evaluated_ast[0]):
            return evaluated_ast[0](*evaluated_ast[1:])  # apply
        return evaluated_ast
    return ast


def eval_ast(ast, env):
    if isinstance(ast, mal_types.MalSymbol):
        v = env.get(ast.data)
        if v is None:
            raise mal_types.MalException("'{}' not found.".format(ast.data))
        return v
    elif isinstance(ast, mal_types.list_types):
        class_type = ast.__class__
        return class_type([EVAL(i, env) for i in ast])
    elif isinstance(ast, mal_types.MalHashMap):
        return mal_types.MalHashMap({EVAL(k, env): EVAL(v, env) for k, v in ast.items()})
    return ast


def PRINT(ast):
    return printer.pr_str(ast)


def rep():
    repl_env = Env()
    repl_env.set('+', lambda a, b: mal_types.MalNumber(a.data + b.data)) # fixme: operate and return maltypes directly
    repl_env.set('-', lambda a, b: mal_types.MalNumber(a.data - b.data))
    repl_env.set('*', lambda a, b: mal_types.MalNumber(a.data * b.data))
    repl_env.set('/', lambda a, b: mal_types.MalNumber((a.data / b.data)))

    while True:
        try:
            print(PRINT(EVAL(READ(input("user> ")), repl_env)))
        except mal_types.MalException as e:
            print(e)
        except Exception as e:
            # raise e
            print(e)

if __name__ == '__main__':
    rep()