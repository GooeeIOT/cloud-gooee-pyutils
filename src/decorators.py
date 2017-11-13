import time


class ExpiredValue(Exception):
    pass


class memoized_expire:

    def __init__(self, ttl):
        """Initialize an empty cache and how long a value will be cached for.

        Each value that is cached corresponds to the parameters of the function it was called with.
        So, my_decorated_func(1) and then a call to my_decorated_func(2) will not hit the cache.
        But, my_decorated_func(1) and then a call to my_decorated_func(1) will hit the cache.

        If you memoize a function where arguments are objects or it's called with a high variety
        of parameters, you might not benifit from memoization!

        :param ttl: How many seconds the value should live for.
        :type ttl: int
        """
        self.cache = {}
        self._validate_ttl(ttl)
        self.ttl = ttl

    def _validate_ttl(self, ttl):
        if not isinstance(ttl, int):
            raise ValueError('memoized_expire only accepts an integer as the "ttl" keyword value.')

    def __call__(self, func):
        def _memoized(*args):
            self.func = func
            now = time.time()
            try:
                value, last_update = self.cache[args]
                age = now - last_update
                if age >= self.ttl:
                    raise ExpiredValue
            except (KeyError, ExpiredValue):
                # Args never cached before or they expired.
                value = self.func(*args)
                self.cache[args] = (value, now)

            return value

        return _memoized
