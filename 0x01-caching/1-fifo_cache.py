#!/usr/bin/env python3
""" BaseCaching module
"""
from datetime import datetime
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    '''Implement the put and get methods of the inherited caching system.
    '''
    def __init__(self):
        super().__init__()
        # create a dictionary for tracking insert/update timestamps
        self.fifo_timestamp = {}

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            # do nothing
            return

        cache_len = len(self.cache_data)

        if cache_len < self.MAX_ITEMS:
            if key not in self.cache_data.keys():
                self.cache_data.update({key: item})
                # create timestamp for the key; timestamps...
                # ...are keys, as keys themselves are values of this dic
                self.fifo_timestamp.update({datetime.utcnow(): key})
            else:
                # key already exists; update
                self.cache_data.update({key: item})
                # replace timestamp of `key` specifically;
                # ...not necessarily the earliest timestamp
                for k, v in self.fifo_timestamp.items():
                    if v == key:
                        del self.fifo_timestamp[k]
                        self.fifo_timestamp.update({datetime.utcnow(): key})
                        break
        else:
            # replacement has to occur if key does not yet exist
            sorted_keys = sorted(self.cache_data.keys())
            if key not in sorted_keys:
                # new key to be inserted
                first_key = sorted(self.fifo_timestamp.keys())[0]  # ascending
                # get the associated cache key
                pop_key = self.fifo_timestamp.get(first_key)
                # replace timestamps, keeping the lifo_timestamp dict trim to 4
                del self.fifo_timestamp[first_key]
                self.fifo_timestamp.update({datetime.utcnow(): key})
                del self.cache_data[pop_key]
                self.cache_data.update({key: item})
                # print('########', pop_key)
                print("DISCARD: {}".format(pop_key))
            else:
                # key exists already; update
                self.cache_data.update({key: item})
                # replace timestamp of `key` specifically;
                # ...not necessarily the earliest timestamp
                for k, v in self.fifo_timestamp.items():
                    if v == key:
                        del self.fifo_timestamp[k]
                        self.fifo_timestamp.update({datetime.utcnow(): key})
                        break

    def get(self, key):
        """ Get an item by key
        """
        if key is None or self.cache_data.get(key, None) is None:
            # do nothing
            return

        return self.cache_data.get(key, None)
