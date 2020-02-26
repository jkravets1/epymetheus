import numpy as np


def wealth(strategy):
    """
    Return time-series of wealth.

    Returns
    -------
    wealth : array, shape (n_bars, )
    """
    # (n_bars, n_assets)
    position = np.concatenate([
        np.zeros((1, strategy.universe.n_assets)),
        np.cumsum(strategy.transaction_matrix, axis=0)[:-1, :],
    ], axis=0)

    # (n_bars, n_assets)
    price_change = np.diff(
        strategy.universe.prices.values,
        axis=0, prepend=0,
    )

    return np.cumsum(
        np.sum(position * price_change, axis=1),
        axis=0,
    )
