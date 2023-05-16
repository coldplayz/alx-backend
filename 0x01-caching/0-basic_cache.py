#!/usr/bin/env python3
""" BaseCaching module
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    '''Implement the put and get methods of the inherited caching system.
    '''
    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None and item is None:
            # do nothing
            return

        self.cache_data.update({key: item})

    def get(self, key):
        """ Get an item by key
        """
        if key is None or self.cache_data.get(key, None) is None:
            # do nothing
            return

        return self.cache_data.get(key, None)
