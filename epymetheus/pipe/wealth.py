import numpy as np


def wealth(strategy):
    """
    Return time-series of wealth.

    Returns
    -------
    wealth : array, shape (n_bars, )
    """
    position = np.cumsum(
        np.stack([
            np.zeros((strategy.universe.n_bars, strategy.n_trades)),
            np.roll(strategy._transaction_matrix, 1, axis=0)[1:, :],
        ]),
        axis=0,
    )
    price_change = np.diff(
        strategy.universe.prices.values,
        axis=0, prepend=0,
    )
    return np.cumsum(
        np.sum(position * price_change, axis=1),
        axis=0,
    )
