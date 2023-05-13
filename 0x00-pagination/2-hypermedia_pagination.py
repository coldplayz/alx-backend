#!/usr/bin/env python3
''' Pagination implementation.
'''
import csv
import math
from typing import List, Tuple, Dict


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

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        '''Returns a dictionary with data implementing HATEOAS.
        '''
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        total_dataset = len(self.dataset())
        data = self.get_page(page, page_size)
        page_size2 = len(data)
        if page_size2 > 0 and total_dataset > (page * page_size):
            next_page = page + 1
        else:
            next_page = None

        if page <= 1:
            prev_page = None
        else:
            prev_page = page - 1

        if (total_dataset % page_size) != 0:
            # decimal fraction quotient
            total_pages = (total_dataset // page_size) + 1
        else:
            total_pages = total_dataset // page_size

        return dict(
                page_size=page_size2,
                page=page,
                data=data,
                next_page=next_page,
                prev_page=prev_page,
                total_pages=total_pages)


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    ''' Returns a tuple of size two containing a start index and an end index.

    This corresponds to the range of indexes to return in a
    ...list for those particular pagination parameters.

    `page` and `page_size` must be greater than zero.
    '''
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
