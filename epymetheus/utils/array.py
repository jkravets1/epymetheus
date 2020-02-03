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


def cross_up(X, threshold=None):
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
    >>> cross_up(X)
    array([[False, False],
           [False,  True],
           [ True, False]])
    >>> cross_up(X, [0, 1])
    array([[False, False],
           [False, False],
           [ True,  True]])
    """
    if threshold is not None:
        return cross_up(X - np.array(threshold))
    return (X > 0) & (np.roll(X, axis=0) <= 0)


def cross_down(X):
    return cross_up(-X)


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
