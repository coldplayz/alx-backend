#!/usr/bin/env python3
""" BaseCaching module
"""
from datetime import datetime
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    '''Implement the put and get methods of the inherited caching system.
    '''
    def __init__(self):
        super().__init__()
        # create a dictionary for tracking insert/update recency
        self.mru_recency = {}
        self.count = 0

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            # do nothing
            return

        cache_len = len(self.cache_data)

        if cache_len < self.MAX_ITEMS:
            self.cache_data.update({key: item})
            # create/update count for the key;
            # integer key for recency dict; `key` as values
            self.count += 1
            self.mru_recency.update({self.count: key})
        else:
            # replacement, or update, has to occur
            sorted_keys = sorted(self.cache_data.keys())
            if key not in sorted_keys:
                # new key to be inserted in both dicts
                mru_key = max(self.mru_recency.keys())
                # get the associated cache key
                pop_key = self.mru_recency.get(mru_key)
                # replace recencies, keeping the mru_recency dict trim to 4
                del self.mru_recency[mru_key]
                self.count += 1
                self.mru_recency.update({self.count: key})

                del self.cache_data[pop_key]
                self.cache_data.update({key: item})
                # print('########', pop_key)
                print("DISCARD: {}".format(pop_key))
            else:
                # key exists already; update
                self.cache_data.update({key: item})
                # replace recency of `key` specifically;
                # ...not necessarily the most recency
                for k, v in self.mru_recency.items():
                    if v == key:
                        del self.mru_recency[k]
                        self.count += 1
                        self.mru_recency.update({self.count: key})
                        break

    def get(self, key):
        """ Get an item by key
        """
        if key is None or self.cache_data.get(key, None) is None:
            # do nothing
            return

        # get is a valid use; update recency
        self.count += 1
        for k, v in self.mru_recency.items():
            if v == key:
                del self.mru_recency[k]
                self.mru_recency.update({self.count: key})
                break

        return self.cache_data.get(key, None)
