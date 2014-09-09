from collections import OrderedDict


class lru_cache(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def __getitem__(self, key):
        value = self.cache[key]
        del self.cache[key]
        self.cache[key] = value

        return value

    def __setitem__(self, key, value):
        if key in self.cache:
            old_value = self[key]
            self.cache[key] = value
        else:
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(False)
