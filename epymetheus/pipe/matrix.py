import numpy as np


def _lot_matrix(strategy):
    """
    Return array representing lot of each asset and trade.

    Parameters
    ----------
    - strategy : Tradestrategy
        Trade strategy with the following attributes:
        * universe
        * trades

    Returns
    -------
    lot_matrix : array, shape (n_assets, n_trades)
        Represent lot of each trede.

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(asset=['Asset0', 'Asset1'], lot=[1, -2], ...),
    ...     Trade(asset='Asset2', lot=3, ...),
    ... ]
    >>> strategy._lot_matrix
    #       Trade0  Trade1
    array([[     1,      0]    # Asset0
           [    -2,      0]    # Asset1
           [     0,      3]])  # Asset2
    """
    return np.stack([
        trade._lot_vector(strategy.universe) for trade in strategy.trades
    ], axis=-1)


def _value_matrix(strategy):
    """
    Return array representing net value of each bar and trade.

    Returns
    -------
    value_matrix : array, shape (n_bars, n_trades)
        Represent value of each trade position.

    Notes
    -----
    All slots are filled even if the coresponding trade is not opening.

    Examples
    --------
    >>> strategy.universe.prices
           Asset0  Asset1  Asset2
    01-01       1      10     100
    01-02       2      20     200
    01-03       3      30     300
    01-04       4      40     400
    01-05       5      50     500
    >>> strategy.trades = [
    ...     Trade(asset=['Asset0', 'Asset1'], lot=[1, -2], ...),
    ...     Trade(asset='Asset2', lot=3, ...),
    ... ]
    >>> strategy._value_matrix
    #       Trade0  Trade1
    array([[   -19,    300]    # 01-01
           [   -38,    600]    # 01-02
           [   -57,    900]    # 01-03
           [   -76,   1200]    # 01-04
           [   -95,   1500]])  # 01-05
    """
    return np.dot(strategy.universe.prices.values, _lot_matrix(strategy))
