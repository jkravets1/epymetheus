import numpy as np

from epymetheus.utils.array import true_since, true_until


def trade_index(strategy):
    """
    Parameters
    ----------
    - strategy : Tradestrategy
        with the following attributes:
        * trades

    Returns
    -------
    trade_index : array, shape (n_orders, )
    """
    return np.repeat(
        np.arange(strategy.n_trades),
        [trade.n_orders for trade in strategy.trades]
    )


def order_index(strategy):
    """
    Parameters
    ----------
    - strategy : Tradestrategy
        with the following attributes:
        * trades

    Returns
    -------
    order_index : array, shape (n_orders, )
    """
    n_orders = sum(trade.n_orders for trade in strategy.trades)
    return np.arange(n_orders)


def assets(strategy):
    return np.concatenate([trade.asset for trade in strategy.trades])


def lots(strategy):
    return np.concatenate([trade.lot for trade in strategy.trades])


def open_bars(strategy):
    return np.repeat(
        [trade.open_bar for trade in strategy.trades],
        [trade.n_orders for trade in strategy.trades]
    )


def close_bars(strategy):
    return np.repeat(
        [trade.close_bar for trade in strategy.trades],
        [trade.n_orders for trade in strategy.trades]
    )


def lot_matrix(strategy):
    """
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
    For the following setup,
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
        trade._lot_vector(strategy.universe)
        for trade in strategy.trades
    ], axis=-1)


def value_matrix(strategy):
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
    >>> history = ...
    >>> history._value_matrix(...)
    array([[   -19,   340],
           [   -38,   680],
           [   -57,  1020],
           [   -76,  1360]])
    """
    return np.dot(strategy.universe.prices, lot_matrix(strategy))


def opening_matrix(strategy):
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
    >>> history = ...
    >>> history._opening_matrix(strategy)
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
