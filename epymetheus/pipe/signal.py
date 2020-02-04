import numpy as np

from ..utils.array import catch_first, cross_up, true_at


def _close_by_signals(strategy):
    """
    Return close_bars from signals.

    Returns
    -------
    close_bars : array, shape (n_trades, )

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
    >>> strategy._acumpnl
    #       Trade0  Trade1
    array([[     0,      0]    # 01-01
           [   -19,      0]    # 01-02
           [   -38,    300]    # 01-03
           [   -38,    600]    # 01-04
           [   -38,    900]])  # 01-05
    >>> strategy.atakes
    array([ 500, 500])
    >>> _closebars_from_signals(strategy)
    array([ 2, 3])
    """
    th_atake = np.array([atake or np.inf for atake in strategy.atakes])

    # n_bars = strategy.universe.n_bars
    # signal_lastbar = np.tile(
    #     true_at(n_bars - 1, n_bars).reshape(n_bars, 1), (1, strategy.n_trades)
    # )

    close_ids = catch_first([
        strategy._signal_closebar,
        strategy._signal_lastbar,
        cross_up(strategy._acumpnl, threshold=th_atake),
    ])
    return close_ids


def _signal_closebar(strategy):
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
        strategy.n_bars,
    )


def _signal_lastbar(strategy):
    """
    Examples
    --------
    >>> strategy.universe.prices
           Asset0  Asset1  Asset2
    01-01       1      10     100
    01-02       2      20     200
    01-03       3      30     300
    01-04       4      40     400
    01-05       5      50     500
    >>> strategy.signal_lastbar
    #       Trade0  Trade1
    array([[ False,  False]    # 01-01
           [ False,  False]    # 01-02
           [ False,  False]    # 01-03
           [ False,  False]    # 01-04
           [  True,   True]])  # 01-05
    """
    signal = np.full((strategy.universe.n_bars, strategy.n_trades), False)
    signal[-1, :] = True
    return signal


def _acumpnl(strategy):
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
    >>> strategy._acumpnl_matrix
    #       Trade0  Trade1
    array([[     0,      0]    # 01-01
           [   -19,      0]    # 01-02
           [   -38,    300]    # 01-03
           [   -38,    600]    # 01-04
           [   -38,    900]])  # 01-05
    """
    value = strategy._value_matrix
    apnl = np.concatenate([
        np.zeros((1, strategy.n_trades)),
        np.diff(value, axis=0),
    ])
    acumpnl = (apnl * strategy._opening_matrix).cumsum(axis=0)
    return acumpnl


def atakes(strategy):
    """
    Return atake of each trade.

    Returns
    -------
    atakes : array, shape (n_trades, )

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(atake=1, asset=['Asset0', 'Asset1'], ...),
    ...     Trade(atake=2, asset=['Asset2'], ...),
    ... ]
    >>> strategy.atakes
    array([ 1, 2])
    """
    return [trade.atake for trade in strategy.trades]


