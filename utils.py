from collections import deque
from itertools import islice, groupby
from operator import itemgetter
from typing import Iterable


def filename_from_path(path):
    import os
    *_parents, file_and_ext = os.path.split(path)
    filename, _ext = os.path.splitext(file_and_ext)
    return filename


def sliding_windows(it: Iterable, n: int):
    it = iter(it)
    window = deque(islice(it, n), maxlen=n)
    assert len(window) == n, f"Iterator passed to `sliding_windows(it, {n})` "\
                             f"had less than {n} elements!"
    yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def unique_justseen(iterable, key=None):
    "List unique elements, preserving order. Remember only the element just seen."
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBCcAD', str.lower) --> A B C A D
    return map(next, map(itemgetter(1), groupby(iterable, key)))


class IterCounter:
    """An iterator wrapping class. Keeps track of the length of the iterator."""
    def __init__(self, it):
        self.it = it
        self.count = None

    def __iter__(self):
        self.count = 0
        for x in self.it:
            self.count += 1
            yield x

    def __len__(self) -> int:
        if self.count is None:
            raise RuntimeError("The `len` of this object is undefined until the "
                               "iterator has been exhausted.")
        return self.count
