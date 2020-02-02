import numpy as np


def wealth(strategy):
    transaction = strategy._transaction_matrix
    t_shift = np.roll(transaction, 1, axis=0)
    t_shift[0, :] = 0
    position = np.cumsum(t_shift, axis=0)
    price_change = np.diff(strategy.universe.prices.values, axis=0, prepend=0)
    return np.sum(np.cumsum(position * price_change, axis=0), axis=1)
