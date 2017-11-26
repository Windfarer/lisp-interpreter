from mal_types import MalException


class Env(object):
    def __init__(self, outer=None):
        self.outer = outer
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def find(self, key):
        if key in self.data:
            return self
        if self.outer is not None:
            return self.outer.find(key)
        raise MalException("'{}' not found.".format(key))

    def get(self, key):
        env = self.find(key)
        if not env:
            raise MalException("'{}' not found.".format(key))
        return env.data[key]