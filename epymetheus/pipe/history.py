import numpy as np


def trade_index(strategy):
    """
    Return order_index of each order.

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
    Return order_index of each order.

    Returns
    -------
    array([0, 1, ..., n_orders - 1]) : shape (n_orders, )
    """
    return np.arange(strategy.n_orders)


def assets(strategy):
    """
    Return asset of each order.

    Returns
    -------
    assets : array, shape (n_orders, )
    """
    if strategy.n_trades == 0:
        return np.array([])
    return np.concatenate([
        trade.asset for trade in strategy.trades
    ])


def lots(strategy):
    """
    Return lot of each order.

    Returns
    -------
    lots : array, shape (n_orders, )
    """
    if strategy.n_trades == 0:
        return np.array([])
    return np.concatenate([
        trade.lot for trade in strategy.trades
    ])


def open_bars(strategy):
    """
    Return open_bar of each order.

    Returns
    -------
    open_bars : array, shape (n_orders, )
    """
    return np.repeat(
        [trade.open_bar for trade in strategy.trades],
        [trade.n_orders for trade in strategy.trades],
    )


def close_bars(strategy):
    """
    Return close_bar of each order.

    Returns
    -------
    close_bars : array, shape (n_orders, )
    """
    return np.repeat(
        [trade.close_bar for trade in strategy.trades],
        [trade.n_orders for trade in strategy.trades],
    )


def close_bars_bysignal(strategy):
    pass


def durations(strategy):
    """
    Return duration of each order.

    Returns
    -------
    durations : array, shape (n_orders, )
    """
    return strategy.close_bars - strategy.open_bars


def open_prices(strategy):
    """
    Return open_price of each order.

    Returns
    -------
    open_prices : array, shape (n_orders, )
    """
    return strategy.universe._pick_prices(strategy.open_bars, strategy.assets)


def close_prices(strategy):
    """
    Return close_price of each order.

    Returns
    -------
    close_prices : array, shape (n_orders, )
    """
    return strategy.universe._pick_prices(strategy.close_bars, strategy.assets)


def gains(strategy):
    """
    Return gain of each order.

    Returns
    -------
    gains : array, shape (n_orders, )
    """
    return (strategy.close_prices - strategy.open_prices) * strategy.lots
