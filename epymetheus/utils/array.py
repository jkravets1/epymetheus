import numpy as np


def catch_first_index(array):
    """
    Examples
    --------
    >>> array = array([ False, False,  True, False,  True])
    >>> catch_first_index(array)
    2

    >>> array = array([ False, False, False, False, False])
    >>> catch_first_index(array)
    -1
    """
    index_true = np.arange(array.size)[array]

    if index_true.size > 0:
        return index_true[0]
    else:
        return -1
