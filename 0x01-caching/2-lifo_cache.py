#!/usr/bin/python3
""" BaseCaching module
"""
from datetime import datetime


class BaseCaching():
    """ BaseCaching defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """
    MAX_ITEMS = 4

    def __init__(self):
        """ Initiliaze
        """
        self.cache_data = {}

    def print_cache(self):
        """ Print the cache
        """
        print("Current cache:")
        for key in sorted(self.cache_data.keys()):
            print("{}: {}".format(key, self.cache_data.get(key)))

    def put(self, key, item):
        """ Add an item in the cache
        """
        raise NotImplementedError(
                "put must be implemented in your cache class")

    def get(self, key):
        """ Get an item by key
        """
        raise NotImplementedError(
                "get must be implemented in your cache class")


class LIFOCache(BaseCaching):
    '''Implement the put and get methods of the inherited caching system.
    '''
    def __init__(self):
        super().__init__()
        # create a dictionary for tracking insert/update timestamps
        self.lifo_timestamp = {}

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None and item is None:
            # do nothing
            return

        cache_len = len(self.cache_data)

        if cache_len < self.MAX_ITEMS:
            self.cache_data.update({key: item})
            # create timestamp for the key;
            # ...timestamps are keys as keys themselves are values of this dic
            self.lifo_timestamp.update({datetime.utcnow(): key})
        else:
            # replacement has to occur if key does not yet exist
            sorted_keys = sorted(self.cache_data.keys())
            if key not in sorted_keys:
                # new key to be inserted in both dicts
                last_key = sorted(self.lifo_timestamp.keys(), reverse=True)[0]
                # get the associated cache key
                pop_key = self.lifo_timestamp.get(last_key)
                # replace timestamps, keeping the lifo_timestamp dict trim to 4
                del self.lifo_timestamp[last_key]
                self.lifo_timestamp.update({datetime.utcnow(): key})
                del self.cache_data[pop_key]
                self.cache_data.update({key: item})
                # print('########', pop_key)
                print("DISCARD: {}".format(pop_key))
            else:
                # key exists already; update
                self.cache_data.update({key: item})
                # replace timestamp of `key` specifically;
                # ...not necessarily the earliest timestamp
                for k, v in self.lifo_timestamp.items():
                    if v == key:
                        del self.lifo_timestamp[k]
                        self.lifo_timestamp.update({datetime.utcnow(): key})
                        break

    def get(self, key):
        """ Get an item by key
        """
        if key is None or self.cache_data.get(key, None) is None:
            # do nothing
            return

        return self.cache_data.get(key, None)
