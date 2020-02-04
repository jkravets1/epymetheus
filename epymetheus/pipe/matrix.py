import numpy as np
from numpy.linalg import multi_dot

from epymetheus.utils.array import true_since, true_until, true_at


def _transaction_matrix(strategy):
    """
    Return array representing transaction at each bar and asset.

    Returns
    -------
    transaction_matrix : array, shape (n_bars, n_assets)

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(
    ...         open_bar='01-01', close_bar='01-03',
    ...         asset=['Asset0', 'Asset1'], lot=[1, -2], ...
    ...     ),
    ...     Trade(
    ...         open_bar='01-02', close_bar='01-05',
    ...         asset='Asset2', lot=3, ...
    ...     ),
    ... ]
    >>> strategy._transaction_matrix
    #       Asset0  Asset1  Asset2
    array([[     1      -2       0]    # 01-01
           [     0       0       3]    # 01-02
           [    -1       2       0]    # 01-03
           [     0       0       0]    # 01-04
           [     0       0      -3]])  # 01-05
    """
    # (n_bars, n_orders) . (n_orders, n_orders) . (n_orders, n_assets)
    return multi_dot([
        strategy.universe._bar_onehot(strategy.open_bars).T
        - strategy.universe._bar_onehot(strategy.close_bars).T,
        np.diag(strategy.lots),
        strategy.universe._asset_onehot(strategy.assets),
    ])


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
    return np.dot(strategy.universe.prices, _lot_matrix(strategy))


def _opening_matrix(strategy):
    """
    Return array whose value is True iff each trade is opening.

    Parameters
    ----------
    - strategy : TradeStrategy
        Necessary atrributes:
        * universe
        * trades

    Returns
    -------
    opening_matrix : array, shape (n_bars, n_trades)
        Represent whether each trade is opening.

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(open_bar='01-01', close_bar='01-03', ...),
    ...     Trade(open_bar='01-02', close_bar='01-05', ...),
    ... ]
    #       Trade0  Trade1
    array([[ False,  False]    # 01-01
           [  True,  False]    # 01-02
           [ False,  False]    # 01-03
           [ False,   True]    # 01-04
           [ False,   True]])  # 01-05
    """
    open_bars = [trade.open_bar for trade in strategy.trades]
    open_ids = strategy.universe._bar_id(open_bars)

    close_bars = [trade.close_bar for trade in strategy.trades]
    close_ids = strategy.universe._bar_id(close_bars)

    return true_since(open_ids + 1, strategy.universe.n_bars) \
        & true_until(close_ids, strategy.universe.n_bars)


def _closebar_matrix(strategy):
    """
    Return an array whose bar is True only when each trade is closed.

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(close_bar='01-03', ...),
    ...     Trade(close_bar='01-05', ...),
    ... ]
    #       Trade0  Trade1
    array([[ False,  False]    # 01-01
           [ False,  False]    # 01-02
           [  True,  False]    # 01-03
           [ False,  False]    # 01-04
           [ False,   True]])  # 01-05
    """
    # TODO make it pipe
    close_bars = [trade.close_bar for trade in strategy.trades]
    return true_at(
        strategy.universe._bar_id(close_bars),
        strategy.n_trades,
    )


def _acumpnl_matrix(strategy):
    """
    Return array representing absolute cumulative p/l of each trade.

    Returns
    -------
    acumpnl : shape (n_bars, n_trades)

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
    ...     Trade(
    ...         open_bar='01-01', close_bar='01-03',
    ...         asset=['Asset0', 'Asset1'], lot=[1, -2], ...
    ...     ),
    ...     Trade(
    ...         open_bar='01-02', close_bar='01-05',
    ...         asset=['Asset2'], lot=3, ...
    ...     ),
    ... ]
    >>> strategy._value_matrix
    #       Trade0  Trade1
    array([[     0,      0]    # 01-01
           [   -19,      0]    # 01-02
           [   -38,    300]    # 01-03
           [   -38,    600]    # 01-04
           [   -38,    900]])  # 01-05
    """
    value = strategy._value_matrix
    apnl = value.diff(axis=0, prepend=value[0, :])
    acumpnl = (apnl * strategy._opening_matrix).cumsum(axis=0)
    return acumpnl
