from functools import wraps
from lru_cache import lru_cache
from pickle import dumps


"""Decorator class for performing automatic memoization."""
class memo(object):
    def __init__(self, cache):
        self.cache = cache

    def __call__(self, func):
        # Decorator to update wrapper to look like func.
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Ensure key is immutable.
            key = dumps((args, kwargs))
            if key not in self.cache:
                self.cache[key] = func(*args, **kwargs)
            return self.cache[key]

        return wrapper


@memo(lru_cache(3))
def fibo(n):
    if n == 0 or n == 1:
        return n
    else:
        return fibo(n - 1) + fibo(n - 2)


def main():
    print fibo(200)


if __name__ == "__main__":
    main()
