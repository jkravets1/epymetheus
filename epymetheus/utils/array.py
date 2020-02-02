import numpy as np


def catch_first(X, fillnan=np.nan):
    """
    Return axis-1 indices for which the values of array are True.

    Parameters
    ----------
    - X : array, shape (m, n)

    Returns
    -------
    - indices : array, shape (m, )

    Examples
    --------
    >>> X
    array([[ True, False, False],
           [False,  True, False],
           [ True, False, False]])
    >>> catch_first(X)
    array([  0,   1, nan])
    >>> catch_first(X, fillnan=-1)
    array([  0,   1,  -1])
    """
    n_samples, n_series = X.shape
    row = np.tile(np.arange(n_samples)[:, np.newaxis], (1, n_series))
    first = np.nanmin(np.where(X, row, n_samples), axis=0)
    first[first == n_samples] = fillnan
    return first


def cutup(X, threshold=None):
    """
    Return array signaling if the series chop up the threshold.

    Parameters
    ----------
    - X : array, shape (n_samples, n_series)
    - threshold : array-like, shape (n_series, ) or None, default None

    Returns
    -------
    - chopup : array, shape (n_samples, n_series)

    Examples
    --------
    >>> X
    array([[ 1, -1],
           [ 0,  1],
           [ 1,  2]])
    >>> cutup(X)
    array([[False, False],
           [False,  True],
           [ True, False]])
    >>> cutup(X, [0, 1])
    array([[False, False],
           [False, False],
           [ True,  True]])
    """
    if threshold is not None:
        return cutup(X - np.array(threshold))
    return (X > 0) & (np.roll(X, axis=0) <= 0)


def cutdown(X):
    return cutup(-X)


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
    n_index = index.size
    index_ = np.tile(index, (n_samples, 1))
    row = np.tile(np.arange(n_samples)[:, np.newaxis], (1, n_index))
    return index_ <= row


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
