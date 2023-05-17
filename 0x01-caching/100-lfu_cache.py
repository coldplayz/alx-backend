#!/usr/bin/env python3
""" BaseCaching module
"""
from datetime import datetime
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    '''Implement the put and get methods of the inherited caching system.
    '''
    def __init__(self):
        super().__init__()
        # create a dictionary for tracking insert/update recency
        self.lru_recency = {}
        self.lfu_frequency = {}
        self.count = 0

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            # do nothing
            return

        cache_len = len(self.cache_data)

        if cache_len < self.MAX_ITEMS:
            # cache not full yet; insert or update
            if key not in self.cache_data.keys():
                # insert
                self.cache_data.update({key: item})
                # track frequency
                self.lfu_frequency.update({key: 1})
                # create/update count for the key;
                # integer key for recency dict; `key` as values
                self.count += 1
                self.lru_recency.update({self.count: key})
            else:
                # key exists already; update
                self.cache_data.update({key: item})
                # track frequency
                self.lfu_frequency.update(
                        {key: self.lfu_frequency.get(key) + 1},
                        )
                # replace recency of `key` specifically;
                # ...not necessarily the earliest recency
                for k, v in self.lru_recency.items():
                    if v == key:
                        del self.lru_recency[k]
                        self.count += 1
                        self.lru_recency.update({self.count: key})
                        break
        else:
            # cache full; replacement, or update, has to occur
            sorted_keys = sorted(self.cache_data.keys())
            if key not in sorted_keys:
                # replacement
                lfu_frq = min(self.lfu_frequency.values())
                if list(self.lfu_frequency.values()).count(lfu_frq) > 1:
                    # multiple least frequencies; dispatch to lru algorithm
                    idx = 0
                    # get lru keys that is ALSO a/the lfu
                    while idx < self.MAX_ITEMS:
                        lru_key = sorted(self.lru_recency)[idx]
                        pop_key = self.lru_recency.get(lru_key)
                        # check if pop_key is also lfu
                        if self.lfu_frequency.get(pop_key) == lfu_frq:
                            # pop_key found
                            break
                        idx += 1
                    # replace recencies, keeping the lru_recency dict trim to 4
                    del self.lru_recency[lru_key]
                    self.count += 1
                    self.lru_recency.update({self.count: key})

                    # update cache
                    del self.cache_data[pop_key]
                    self.cache_data.update({key: item})
                    # replace frequency
                    del self.lfu_frequency[pop_key]
                    self.lfu_frequency.update({key: 1})
                else:
                    # single least frequency
                    self.cache_data.update({key: item})
                    # update frequency
                    for k, v in self.lfu_frequency.items():
                        if v == lfu_frq:
                            pop_key = k
                            # replace in cache
                            del self.cache_data[pop_key]
                            # replace frequency
                            del self.lfu_frequency[pop_key]
                            self.lfu_frequency.update({key: 1})
                            break
                    # replace recencies, keeping the lru_recency dict trim to 4
                    lru_key = min(self.lru_recency.keys())
                    del self.lru_recency[lru_key]
                    self.count += 1
                    self.lru_recency.update({self.count: key})
                # print('########', pop_key)
                print("DISCARD: {}".format(pop_key))
            else:
                # key exists already; update
                self.cache_data.update({key: item})
                # update frequency
                self.lfu_frequency.update(
                        {key: self.lfu_frequency.get(key) + 1},
                        )
                # replace recency of `key` specifically;
                # ...not necessarily the earliest recency
                for k, v in self.lru_recency.items():
                    if v == key:
                        del self.lru_recency[k]
                        self.count += 1
                        self.lru_recency.update({self.count: key})
                        break

    def get(self, key):
        """ Get an item by key
        """
        if key is None or self.cache_data.get(key, None) is None:
            # do nothing
            return

        # get is a valid use; update recency
        self.count += 1
        for k, v in self.lru_recency.items():
            if v == key:
                del self.lru_recency[k]
                self.lru_recency.update({self.count: key})
                break

        # update frequency
        self.lfu_frequency.update(
                {key: self.lfu_frequency.get(key) + 1},
                )

        return self.cache_data.get(key, None)
