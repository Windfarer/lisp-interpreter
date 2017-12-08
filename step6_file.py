import reader
import printer
import mal_types
from env import Env
from core import ns

repl_env = Env()
for k, v in ns.items():
    repl_env.set(k, v)

def READ(string):
    return reader.read_str(string)


def EVAL(ast, env):
    while True:
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
                    ast, env = ast[2], let_env
                    continue

                elif ast[0].data == 'do':
                    ast = eval_ast(ast[1:], env)[-1]
                    continue

                elif ast[0].data == 'if':
                    if EVAL(ast[1], env):
                        ast = ast[2]
                        continue
                    else:
                        if len(ast) == 4:
                            ast = ast[3]
                            continue
                        return mal_types.MalNil()

                elif ast[0].data == 'fn*':
                    def fn(*exprs):
                        new_env = Env(outer=env, binds=ast[1], exprs=exprs)
                        return EVAL(ast[2], new_env)
                    return mal_types.MalFn(ast=ast[2], params=ast[1], env=env, fn=fn)

                elif ast[0].data == 'eval':
                    return lambda ast: EVAL(ast[1:], repl_env)

            # apply
            evaluated_ast = eval_ast(ast, env)
            if callable(evaluated_ast[0]):
                f, args = evaluated_ast[0], evaluated_ast[1:]
                if isinstance(f, mal_types.MalFn):
                    ast= f.ast
                    env = Env(outer=f.env, binds=f.params, exprs=args)
                    # print(f)
                    continue
                else:
                    return f(*args)
            return evaluated_ast
        return mal_types.MalNil()


def eval_ast(ast, env):
    # print('find', ast)
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


def rep(input):
    return PRINT(EVAL(READ(input), repl_env))


def main():
    rep('"(def! load-file (fn* (f) (eval (read-string (str"(do" (slurp f) ")")))))"')
    while True:
        try:
            print(rep(input("user> ")))
        except mal_types.MalException as e:
            # raise e
            print(e)
        except Exception as e:
            # raise e
            print(e)

if __name__ == '__main__':
    main()