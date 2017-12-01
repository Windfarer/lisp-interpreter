import reader
import printer
import mal_types
from env import Env
from core import ns

def READ(string):
    return reader.read_str(string)


def EVAL(ast, env):
    if not isinstance(ast, mal_types.MalList):
        return eval_ast(ast, env)
    elif not ast:
        return ast
    elif isinstance(ast, mal_types.MalList):
        if isinstance(ast[0], mal_types.MalSymbol):
            if ast[0].data == 'def!':
                value = EVAL(ast[2], env)
                env.set(ast[1].data, value)
                return value
            elif  ast[0].data == 'let*':
                let_env = Env(outer=env)
                for k ,v in  zip(ast[1][::2], ast[1][1::2]):
                    let_env.set(k, EVAL(v, let_env))
                return EVAL(ast[2], let_env)
            elif ast[0].data == 'do':
                return eval_ast(ast[1:], env)
            elif ast[0].data == 'if':
                if EVAL(ast[1], env):
                    return EVAL(ast[2], env)
                else:
                    if len(ast) > 2:
                        return EVAL(ast[3], env)
                    else:
                        return mal_types.MalNil()
            elif ast[0].data == 'fn*':
                def closure(*exprs):
                    new_env = Env(outer=env, binds=ast[1], exprs=exprs)
                    # print(new_env.data)
                    # print(ast[2])
                    return EVAL(ast[2], new_env)
                return closure
        evaluated_ast = eval_ast(ast, env)
        if callable(evaluated_ast[0]):
            return evaluated_ast[0](*evaluated_ast[1:])  # apply
        return evaluated_ast
    return ast


def eval_ast(ast, env):
    # print('find', type(ast), )
    if isinstance(ast, mal_types.MalSymbol):
        v = env.get(ast)
        if not v:
            raise mal_types.MalException("'{}' not found.".format(ast.data))
        return v
    elif isinstance(ast, mal_types.MalList):
        return mal_types.MalList([EVAL(i, env) for i in ast])
    return ast


def PRINT(ast):
    return printer.pr_str(ast)


def rep():
    repl_env = Env()
    for k, v in ns.items():
        repl_env.set(k, v)

    while True:
        try:
            print(PRINT(EVAL(READ(input("user> ")), repl_env)))
        except mal_types.MalException as e:
            print(e)


if __name__ == '__main__':
    rep()