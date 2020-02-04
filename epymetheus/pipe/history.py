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

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(asset=['Asset0', 'Asset1'], ...),
    ...     Trade(asset=['Asset2'], ...),
    ... ]
    >>> strategy.trade_index
    array([ 0, 0, 1])
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

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(asset=['Asset0', 'Asset1'], ...),
    ...     Trade(asset=['Asset2'], ...),
    ... ]
    >>> strategy.trade_index
    array([ 0, 1, 2])
    """
    return np.arange(strategy.n_orders)


def asset_ids(strategy):
    """
    Return asset id of each order.

    Returns
    -------
    asset_ids : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.universe.assets
    >>> Index(['Asset0', 'Asset1', 'Asset2', ...])
    >>> strategy.trades = [
    ...     Trade(asset=['Asset0', 'Asset1'], ...),
    ...     Trade(asset=['Asset2'], ...),
    ... ]
    >>> strategy.assets
    array([ 0, 1, 2])
    """
    return strategy.universe.assets.get_indexer(
        np.concatenate([
            trade.asset for trade in strategy.trades
        ])
    )


def lots(strategy):
    """
    Return lot of each order.

    Returns
    -------
    lots : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(lot=[1, -2], ...),
    ...     Trade(lot=[3], ...),
    ... ]
    >>> strategy.lots
    array([  1, -2,  3])
    """
    return np.concatenate([
        trade.lot for trade in strategy.trades
    ])


def open_bar_ids(strategy):
    """
    Return open_bar of each order.

    Returns
    -------
    open_bar_ids : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.universe.bars
    Index(['01-01', '01-02', '01-03', ...])
    >>> strategy.trades = [
    ...     Trade(open_bar='01-01', asset=['Asset0', 'Asset1'], ...),
    ...     Trade(open_bar='01-02', asset=['Asset2'], ...),
    ... ]
    >>> strategy.open_bar_ids
    array([ 1, 1, 2])
    """
    def ifnonefirst(bar):
        if bar is None:
            return strategy.universe.bars[0]
        else:
            return bar
    open_bars = [ifnonefirst(trade.open_bar) for trade in strategy.trades]
    return strategy.universe._bar_id(np.repeat(
        open_bars, [trade.n_orders for trade in strategy.trades],
    ))


def close_bar_ids(strategy):
    """
    Return close_bar of each order.

    Returns
    -------
    close_bars : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(close_bar='01-01', asset=['Asset0', 'Asset1'], ...),
    ...     Trade(close_bar='01-02', asset=['Asset2'], ...),
    ... ]
    >>> strategy.close_bars
    array([ 1, 1, 2])
    """
    def ifnonelast(bar):
        if bar is None:
            return strategy.universe.bars[-1]
        else:
            return bar
    close_bars = [ifnonelast(trade.close_bar) for trade in strategy.trades]
    return strategy.universe._bar_id(np.repeat(
        close_bars, [trade.n_orders for trade in strategy.trades],
    ))


def durations(strategy):
    """
    Return duration of each order.

    Returns
    -------
    durations : array, shape (n_orders, )

    Examples
    --------
    With '01-01' denoting datetime object with subtraction operation,
    >>> strategy.trades = [
    ...     Trade(
    ...         open_bar='01-01', close_bar='01-03',
    ...         asset=['Asset0', 'Asset1'], ...
    ...     ),
    ...     Trade(
    ...         open_bar='01-02', close_bar='01-05',
    ...         asset=['Asset2'], ...
    ...     ),
    ... ]
    >>> strategy.durations
    array([ 2days, 2days, 3days])
    """
    return strategy.close_bars - strategy.open_bars


def open_prices(strategy):
    """
    Return open_price of each order.

    Returns
    -------
    open_prices : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.universe
           Asset0  Asset1  Asset2
    01-01       1      10     100
    01-02       2      20     200
    >>> strategy.trades = [
    ...     Trade(open_bar='01-01', asset=['Asset0', 'Asset1'], ...),
    ...     Trade(open_bar='01-02', asset=['Asset2'], ...),
    ... ]
    >>> strategy.open_prices
    array([  1,  10, 200]
    """
    return strategy.universe._pick_prices(
        strategy.open_bar_ids, strategy.asset_ids
    )


def close_prices(strategy):
    """
    Return close_price of each order.

    Returns
    -------
    close_prices : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.universe
           Asset0  Asset1  Asset2
    01-01       1      10     100
    01-02       2      20     200
    >>> strategy.trades = [
    ...     Trade(close_bar='01-01', asset=['Asset0', 'Asset1'], ...),
    ...     Trade(close_bar='01-02', asset=['Asset2'], ...),
    ... ]
    >>> strategy.close_prices
    array([  1,  10, 200]
    """
    return strategy.universe._pick_prices(
        strategy.close_bar_ids, strategy.asset_ids
    )


def gains(strategy):
    """
    Return gain of each order.

    Returns
    -------
    gains : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.universe
           Asset0  Asset1  Asset2
    01-01       1      10     100
    01-02       2      20     200
    01-03       3      30     300
    01-04       4      40     400
    01-05       5      50     500
    >>> strategy.trades = [
    ...     Trade(
    ...         open_bar='01-01', close_bar='01-03',
    ...         asset=['Asset0', 'Asset1'], ...
    ...     ),
    ...     Trade(
    ...         open_bar='01-02', close_bar='01-05',
    ...         asset=['Asset2'], ...
    ...     ),
    ... ]
    >>> strategy.gains
    array([  2,  20, 300])
    """
    return (strategy.close_prices - strategy.open_prices) * strategy.lots