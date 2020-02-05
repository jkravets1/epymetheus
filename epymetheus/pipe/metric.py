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
