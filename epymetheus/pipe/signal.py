import numpy as np

from ..utils.array import catch_first, cross_up, true_at


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
    >>> strategy._acumpnl_matrix
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
    th_atake = [atake or np.inf for atake in strategy.atakes]

    # cross_up(strategy._acumpnl_matrix, threshold=th_atake),
    print(strategy._closebar_matrix)
    close_ids = catch_first([
        strategy._closebar_matrix,
    ])
    return strategy.universe.bars[close_ids]
