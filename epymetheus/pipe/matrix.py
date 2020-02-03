import numpy as np
from numpy.linalg import multi_dot

from epymetheus.utils.array import true_since, true_until, true_at


def _transaction_matrix(strategy):
    """
    Represent transaction at each bar and asset.

    Returns
    -------
    transaction_matrix : array, shape (n_bars, n_assets)

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(asset='AAPL', open_bar='Bar1', lot=2),
    ...     Trade(asset=['AAPL', 'MSFT'], open_bar='Bar1', lot=[3, 4]),
    ... ]
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
    Represent lot of each asset and trade.

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
    >>> universe.assets
    Index(['AAPL', 'MSFT', 'AMZN'], dtype='object')
    >>> trade0 = Trade(['AAPL', 'MSFT'], lot=[1, -2], ...)
    >>> trade1 = Trade(['AMZN', 'MSFT'], lot=[3,  4], ...)
    >>> strategy.universe = universe
    >>> strategy.trades = [trade0, trade1]
    >>> lot_matrix(strategy)
    array([[ 1,  0],
           [-2,  4],
           [ 0,  3]])
    """
    return np.stack([
        trade._lot_vector(strategy.universe) for trade in strategy.trades
    ], axis=-1)


def _value_matrix(strategy):
    """
    Returns
    -------
    value_matrix : array, shape (n_bars, n_trades)
        Represent value of each trade position.

    Examples
    --------
    >>> universe.assets
    Index(['AAPL', 'MSFT', 'AMZN'], dtype='object')
    >>> trade0 = Trade(['AAPL', 'MSFT'], lot=[1, -2], ...)
    >>> trade1 = Trade(['AMZN', 'MSFT'], lot=[3,  4], ...)
    >>> universe.prices
    array([[  1,  10, 100],
           [  2,  20, 200],
           [  3,  30, 300],
           [  4,  40, 400]])
    >>> value_matrix(...)
    array([[   -19,   340],
           [   -38,   680],
           [   -57,  1020],
           [   -76,  1360]])
    """
    return np.dot(strategy.universe.prices, _lot_matrix(strategy))


def _opening_matrix(strategy):
    """
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
    >>> universe.assets
    Index(['01-01', '01-02', '01-03'], dtype='object')
    >>> trade0 = Trade(..., open_bar='01-01', close_bar='01-02')
    >>> trade1 = Trade(..., open_bar='01-01', close_bar='01-03')
    >>> strategy.trades = [trade0, trade1]
    >>> opening_matrix(strategy)
    array([[False, False],
           [ True,  True],
           [False,  True]])
    """
    open_bars = [trade.open_bar for trade in strategy.trades]
    open_ids = strategy.universe._bar_id(open_bars)

    close_bars = [trade.close_bar for trade in strategy.trades]
    close_ids = strategy.universe._bar_id(close_bars)

    return true_since(open_ids + 1, strategy.universe.n_bars) \
        & true_until(close_ids, strategy.universe.n_bars)


def _closebar_matrix(strategy):
    """
    Examples
    --------
    >>> universe.assets
    Index(['01-01', '01-02', '01-03'], dtype='object')
    >>> trade0 = Trade(..., open_bar='01-01', close_bar='01-02')
    >>> trade1 = Trade(..., open_bar='01-01', close_bar='01-03')
    >>> strategy.trades = [trade0, trade1]
    >>> opening_matrix(strategy)
    array([[False, False],
           [False,  True],
           [ True, False]])
    """
    close_bars = [trade.close_bar for trade in strategy.trades]
    closebar_ids = strategy.universe._bar_id(close_bars)
    return true_at(closebar_ids, strategy.n_trades)


def _acumpnl_matrix(strategy):
    """
    Return absolute cumulative profit and loss of each trade

    Returns
    -------
    acumpnl : shape (n_nars, n_trades)
    """
    value = _value_matrix(strategy)
    opening = _opening_matrix(strategy)
    apnl = value.diff(axis=0, prepend=value[0, :])
    acumpnl = (apnl * opening).cumsum(axis=0)
    return acumpnl
