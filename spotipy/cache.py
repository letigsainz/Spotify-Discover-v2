from cachetools import Cache, TTLCache


class TokenCache(TTLCache):
    """Overriding TTL cache to allow for setting a per-item TTL"""
    def __init__(self):
        self.cache = super().__init__(maxsize=128, ttl=8600)

    def __setitem__(self, key, value, ttl, cache_setitem=Cache.__setitem__):
        super(TokenCache, self).__setitem__(key, value)
        link = self._TTLCache__links.get(key, None)
        if link:
            link.expires += ttl - self.ttl - 1
        return link.expires

    def save_token(self, key, value, ttl):
        return self.__setitem__(key, value, ttl)

    def get_token(self, key):
        return self.get(key)
