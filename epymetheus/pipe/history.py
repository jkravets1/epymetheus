import numpy as np


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
    return np.arange(strategy.n_orders)


def assets(strategy):
    """
    Parameters
    ----------
    strategy : TradeStrategy
        with the following attributes:
        * trades
    """
    if strategy.n_trades == 0:
        return np.array([])
    return np.concatenate([trade.asset for trade in strategy.trades])


def lots(strategy):
    if strategy.n_trades == 0:
        return np.array([])
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

def close_bars_bysignal(strategy):
    pass


def durations(strategy):
    return strategy.close_bars - strategy.open_bars


def open_prices(strategy):
    return strategy.universe._pick_prices(strategy.open_bars, strategy.assets)


def close_prices(strategy):
    return strategy.universe._pick_prices(strategy.close_bars, strategy.assets)


def gains(strategy):
    return (strategy.close_prices - strategy.open_prices) * strategy.lots
