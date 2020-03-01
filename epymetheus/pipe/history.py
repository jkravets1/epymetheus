import numpy as np


def open_bar_ids(strategy, columns='trades'):
    """
    Return open_bar of each trade/order.

    Parameters
    ----------
    - strategy
    - columns : {'trades', 'orders'}, default 'trades'

    Returns
    -------
    If columns = 'trades' :
        open_bar_ids : array, shape (n_trades, )
    If columns = 'orders' :
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
    array([ 1, 2])
    """
    if columns == 'orders':
        return np.repeat(
            open_bar_ids(strategy, columns='trades'),
            [trade.n_orders for trade in strategy.trades],
        )

    def ifnonefirst(bar):
        if bar is None:
            return strategy.universe.bars[0]
        else:
            return bar
    open_bars = [ifnonefirst(trade.open_bar) for trade in strategy.trades]
    return strategy.universe._bar_id(open_bars)


def shut_bar_ids(strategy, columns='trades'):
    """
    Return shut_bar of each trade/order.

    Returns
    -------
    If columns = 'trades' :
        open_bar_ids : array, shape (n_trades, )
    If columns = 'orders' :
        open_bar_ids : array, shape (n_orders, )
    shut_bars : array, shape (n_trades, )

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(shut_bar='01-01', asset=['Asset0', 'Asset1'], ...),
    ...     Trade(shut_bar='01-02', asset=['Asset2'], ...),
    ... ]
    >>> strategy.shut_bars
    array([ 1, 2])
    """
    if columns == 'orders':
        return np.repeat(
            shut_bar_ids(strategy, columns='trades'),
            [trade.n_orders for trade in strategy.trades],
        )

    def ifnonelast(bar):
        if bar is None:
            return strategy.universe.bars[-1]
        else:
            return bar
    shut_bars = [ifnonelast(trade.shut_bar) for trade in strategy.trades]
    return strategy.universe._bar_id(shut_bars)


def takes(strategy, columns='trades'):
    """
    Return take of each trade.

    Returns
    -------
    If columns = 'trades' :
        takes : array, shape (n_trades, )
    If columns = 'orders' :
        takes : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(take=1, asset=['Asset0', 'Asset1'], ...),
    ...     Trade(take=2, asset=['Asset2'], ...),
    ... ]
    >>> strategy.takes
    array([ 1, 2])
    """
    if columns == 'orders':
        return np.repeat(
            takes(strategy, columns='trades'),
            [trade.n_orders for trade in strategy.trades],
        )
    return np.array([trade.take or np.inf for trade in strategy.trades])


def stops(strategy, columns='trades'):
    """
    Return stop of each trade.

    Parameters
    ----------
    - strategy
    - columns

    Returns
    -------
    If columns = 'trades' :
        stops : array, shape (n_trades, )
    If columns = 'orders' :
        stops : array, shape (n_orders, )

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(stop=-1, asset=['Asset0', 'Asset1'], ...),
    ...     Trade(stop=-2, asset=['Asset2'], ...),
    ... ]
    >>> strategy.stop
    array([ -1, -2])
    """
    if columns == 'orders':
        return np.repeat(
            stops(strategy, columns='trades'),
            [trade.n_orders for trade in strategy.trades],
        )
    return np.array([trade.stop or -np.inf for trade in strategy.trades])


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
    ...         open_bar='01-01', shut_bar='01-03',
    ...         asset=['Asset0', 'Asset1'], ...
    ...     ),
    ...     Trade(
    ...         open_bar='01-02', shut_bar='01-05',
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
        strategy.open_bar_ids, strategy.asset_id
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
    ...     Trade(shut_bar='01-01', asset=['Asset0', 'Asset1'], ...),
    ...     Trade(shut_bar='01-02', asset=['Asset2'], ...),
    ... ]
    >>> strategy.close_prices
    array([  1,  10, 200]
    """
    return strategy.universe._pick_prices(
        strategy.close_bar_ids, strategy.asset_id
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
    ...         open_bar='01-01', shut_bar='01-03',
    ...         asset=['Asset0', 'Asset1'], ...
    ...     ),
    ...     Trade(
    ...         open_bar='01-02', shut_bar='01-05',
    ...         asset=['Asset2'], ...
    ...     ),
    ... ]
    >>> strategy.gains
    array([  2,  20, 300])
    """
    return (strategy.close_prices - strategy.open_prices) * strategy.lot
