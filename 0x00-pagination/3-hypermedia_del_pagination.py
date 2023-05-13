#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        '''Implements deletion-resilient hypermedia pagination.

        The goal here is that if between two queries, certain rows are
        ...removed from the dataset,
        ...the user does not miss items from dataset when changing page.
        '''
        dataset_size = len(self.__indexed_dataset)

        assert index is not None and dataset_size > index
        assert isinstance(index, int) and isinstance(page_size, int)

        next_idx = index
        end = None
        data = []
        page_len = page_size

        while page_len != 0 and dataset_size > next_idx:
            # fetch the required number of data items/rows
            row = self.indexed_dataset().get(next_idx, None)
            if row:
                data.append(row)
                next_idx += 1
                page_len -= 1
            else:
                # possibly deleted item; go to next
                next_idx += 1

        return dict(
                index=index,
                next_index=(next_idx if dataset_size > next_idx else None),
                page_size=len(data),
                data=data,
                )
