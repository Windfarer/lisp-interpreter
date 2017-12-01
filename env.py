from mal_types import MalException, MalSymbol


class Env(object):
    def __init__(self, outer=None, binds=None, exprs=None):
        self.outer = outer
        self.data = {}
        if binds is None:
            binds = []
        if exprs is None:
            exprs = []
        for bind, expr in zip(binds, exprs):
            self.set(bind, expr)

    def set(self, key, value):
        if isinstance(key, MalSymbol):
            key = key.data
        self.data[key] = value

    def find(self, key):
        if key in self.data:
            return self
        if self.outer is not None:
            return self.outer.find(key)
        raise MalException("'{}' not found.".format(key))

    def get(self, key):
        if isinstance(key, MalSymbol):
            key = key.data
        env = self.find(key)
        return env.data[key]