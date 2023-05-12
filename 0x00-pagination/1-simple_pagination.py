#!/usr/bin/env python3
''' Pagination implementation.
'''
import csv
import math
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''Return the appropriate page [list or rows] of the dataset.
        '''
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        start, end = index_range(page, page_size)
        if end >= len(self.dataset()):
            # out of bounds/range of dataset list
            return []
        return self.dataset()[start:end]



def index_range(page: int, page_size: int) -> Tuple[int, int]:
    ''' Returns a tuple of size two containing a start index and an end index.

    This corresponds to the range of indexes to return in a
    ...list for those particular pagination parameters.

    `page` and `page_size` must be greater than zero.
    '''
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
