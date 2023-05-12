#!/usr/bin/env python3
''' Pagination.
'''
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    ''' Returns a tuple of size two containing a start index and an end index.

    This corresponds to the range of indexes to return in a
    ...list for those particular pagination parameters.

    `page` and `page_size` must be greater than zero.
    '''
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
