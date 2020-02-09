import numpy as np


def net_exposure(strategy):
    """
    Returns
    -------
    - net_exposure : array, shape (n_bars, )
    """
    net_position = np.cumsum(strategy.transaction_matrix, axis=0)
    return np.sum(net_position * strategy.universe.prices.values, axis=1)


def abs_exposure(strategy):
    """
    Returns
    -------
    - net_exposure : array, shape (n_bars, )
    """
    abs_position = np.abs(np.cumsum(strategy.transaction_matrix, axis=0))
    return np.sum(abs_position * strategy.universe.prices.values, axis=1)


def volatility(strategy):
    """
    Return unbiased standard deviation of gains per bars.

    Returns
    -------
    - volatility : float
    """
    return np.std(np.diff(strategy.wealth.wealth), ddof=1)


def drop(strategy):
    """
    Return drop of the wealth from its cumulative max.

    Returns
    -------
    - drop : array, shape (n_bars, )

    Examples
    --------
    >>> strategy.wealth
    array([0, 1, 2, 1, 0])
    >>> strategy.drop
    array([0, 0, 0, -1, -2])
    """
    return strategy.wealth.wealth - np.maximum.accumulate(strategy.wealth.wealth)


def max_drop(strategy):
    """
    Return maximum drop of the wealth from its cumulative max.

    Returns
    -------
    - max_drop : float
        Maximum drop. always non-positive.

    Examples
    --------
    >>> strategy.wealth
    array([0, 1, 2, 1, 0])
    >>> strategy.drop
    array([0, 0, 0, -1, -2])
    >>> strategy.max_drop
    -2
    """
    return min(drop(strategy))
