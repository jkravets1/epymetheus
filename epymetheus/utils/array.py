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



# def catch_first(arrays):
#     """
#     Return axis-1 indices for which the values of array are True.
#     If all false, filled with n_samples.

#     Parameters
#     ----------
#     - arrays : sequence of array-like, shape (n_samples, n_series) each
#         Each array must have the same shape.

#     Returns
#     -------
#     - indices : array, shape (n_series, )
#         First indices to make any of arrays True.

#     Examples
#     --------
#     One array:
#     >>> a
#     array([[ True, False, False],
#            [False,  True, False],
#            [ True, False, False]])
#     >>> catch_first([a])
#     array([  0,   1, nan])
#     >>> catch_first(a, fillna=-1)
#     array([  0,   1,  -1])

#     Multiple arrays:
#     >>> b
#     array([[False,  True, False],
#            [False, False,  True],
#            [ True, False, False]])
#     >>> catch_first([a, b])
#     array([  0,   0,   1])
#     """
#     X = np.logical_or.reduce(arrays)
#     n_samples, n_series = X.shape
#     row = np.tile(np.arange(n_samples)[:, np.newaxis], (1, n_series))
#     first = np.nanmin(np.where(X, row, n_samples), axis=0)
#     return first


def cross_up(array, threshold=None):
    """
    Return array signaling if the series chop up the threshold.

    Parameters
    ----------
    - array : array, shape (n_samples, n_series)
        Each array must have the same shape.
    - threshold : float or array-like, shape (n_series, ), default 0
        Threshold to cross up.

    Returns
    -------
    - cross_up : array, shape (n_samples, n_series)

    Examples
    --------
    >>> a
    array([[ 1, -1],
           [ 0,  1],
           [ 1,  2]])
    >>> cross_up(a)
    array([[False, False],
           [False,  True],
           [ True, False]])
    >>> cross_up(a, [0, 1])
    array([[False, False],
           [False, False],
           [ True,  True]])
    """
    if threshold is not None:
        return cross_up(array - threshold, threshold=None)

    n_samples, n_series = array.shape
    return np.concatenate([
        np.full((1, n_series), False),
        (array[1:] > 0) & (array[:-1] <= 0),
    ])


def cross_down(array, threshold=None):
    if threshold is not None:
        threshold = -threshold
    return cross_up(-array, threshold)


def true_since(index, n_samples):
    """
    Examples
    --------
    >>> index
    array([  1,  0,  5, -1])
    >>> true_since(index, 3)
    array([[False,  True, False,  True],
           [ True,  True, False,  True],
           [ True,  True, False,  True]])
    """
    n0, n1 = n_samples, index.size
    return np.tile(index, (n0, 1)) <= row(shape=(n0, n1))


def true_until(index, n_samples):
    """
    Examples
    --------
    >>> index
    array([  1,  0,  5, -1])
    >>> true_since(index, 3)
    array([[ True,  True,  True, False],
           [ True, False,  True, False],
           [False, False,  True, False]])
    """
    return ~true_since(index + 1, n_samples)


def row(shape):
    """
    Examples
    --------
    >>> row(shape=(3, 4))
    array([[ 0 0 0 0]
           [ 1 1 1 1]
           [ 2 2 2 2]])
    """
    n0, n1 = shape
    return np.tile(np.arange(n0)[:, np.newaxis], (1, n1))


def true_at(index, n_samples):
    """
    Examples
    --------
    >>> index
    array([  1,  0,  5, -1])
    >>> true_since(index, 3)
    array([[False,  True, False, False],
           [ True, False, False, False],
           [False, False, False, False]])
    """
    n0, n1 = n_samples, index.size
    return np.tile(index, (n0, 1)) == row(shape=(n0, n1))
