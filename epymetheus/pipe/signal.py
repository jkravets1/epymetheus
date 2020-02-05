import numpy as np

from epymetheus.utils.array import (
    catch_first,
    cross_up,
    cross_down,
    true_at,
    true_since,
    true_until,
)
from epymetheus.pipe.matrix import _value_matrix
from epymetheus.pipe.history import open_bar_ids, shut_bar_ids, atakes, acuts


def _close_bar_ids_from_signals(strategy, columns='trades'):
    """
    Return close_bar of each trade from signals.

    Returns
    -------
    closebar_ids : array, shape (n_trades, )

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
    ...         open_bar='01-01', shut_bar='01-03',
    ...         asset=['Asset0', 'Asset1'], lot=[1, -2], ...
    ...     ),
    ...     Trade(
    ...         open_bar='01-02', shut_bar='01-05',
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
    if columns == 'orders':
        return np.repeat(
            _close_bar_ids_from_signals(strategy, columns='trades'),
            [trade.n_orders for trade in strategy.trades],
        )

    th_atakes = atakes(strategy, columns='trades')
    th_acuts = acuts(strategy, columns='trades')

    return catch_first([
        _signal_shutbar(strategy),
        _signal_lastbar(strategy),
        cross_up(_acumpnl(strategy), threshold=th_atakes),
        cross_down(_acumpnl(strategy), threshold=th_acuts),
    ])


def _signal_shutbar(strategy):
    """
    Return an array whose bar is True only when each trade is shut.

    Returns
    -------
    signal_shutbar : array, shape (n_bars, n_trades)

    Examples
    --------
    >>> strategy.trades = [
    ...     Trade(shut_bar='01-03', ...),
    ...     Trade(shut_bar='01-05', ...),
    ... ]
    #       Trade0  Trade1
    array([[ False,  False]    # 01-01
           [ False,  False]    # 01-02
           [  True,  False]    # 01-03
           [ False,  False]    # 01-04
           [ False,   True]])  # 01-05
    """
    # TODO make it pipe
    shutbar_ids = strategy.universe._bar_id([
        trade.shut_bar for trade in strategy.trades
    ])
    return true_at(shutbar_ids, strategy.n_bars)


def _signal_lastbar(strategy):
    """
    Returns
    -------
    signal_lastbar : array, shape (n_bars, n_trades)

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


def _signal_opening(strategy):
    """
    Return array whose value is True iff each trade has been opened
    and has not been shut.

    Notes
    -----
    It is True until each trade is shut, not until each trade is closed.

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
    op = open_bar_ids(strategy, columns='trades')  # (n_bars, n_trades)
    sh = shut_bar_ids(strategy, columns='trades')  # (n_bars, n_trades)

    return true_since(op + 1, strategy.universe.n_bars) \
        & true_until(sh, strategy.universe.n_bars)


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
    ...         open_bar='01-01', shut_bar='01-03',
    ...         asset=['Asset0', 'Asset1'], lot=[1, -2], ...
    ...     ),
    ...     Trade(
    ...         open_bar='01-02', shut_bar='01-05',
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
    value = _value_matrix(strategy)
    apnl = np.concatenate([
        np.zeros((1, strategy.n_trades)),
        np.diff(value, axis=0),
    ])
    acumpnl = (apnl * _signal_opening(strategy)).cumsum(axis=0)
    return acumpnl
