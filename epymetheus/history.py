from time import time

import numpy as np

from epymetheus.utils import TradeResult


class History(TradeResult):
    """
    Represent trade history.

    Attributes
    ----------
    - order_index : numpy.array, shape (n_orders, )
        Indices of orders.
    - trade_index : numpy.array, shape (n_orders, )
        Indices of trades.
        If multiple orders has been made in a single trade, the same index
        will be assigned for these orders.
    - assets : numpy.array, shape (n_orders, )
    - lots : numpy.array, shape (n_orders, )
    - open_bars : numpy.array, shape (n_orders, )
    - close_bars : numpy.array, shape (n_orders, )
    - durations : numpy.array, shape (n_orders, )
    - open_prices : numpy.array, shape (n_orders, )
    - close_prices : numpy.array, shape (n_orders, )
    - gains : numpy.array, shape (n_orders, )

    Examples
    --------
    >>> ...
    """
    @classmethod
    def from_strategy(cls, strategy, verbose=True):
        """
        Initialize self from strategy.

        Parameters
        ----------
        - strategy : TradeStrategy
        - verbose : bool

        Returns
        -------
        history : History
        """
        if verbose:
            msg = 'Evaluating history'
            print(f'{msg:<22} ... ', end='')
            begin_time = time()

        history = cls()
        history.trade_index = cls._get_trade_index(strategy)
        history.order_index = cls._get_order_index(strategy)

        history.asset = cls._get_asset(strategy)
        history.lot = cls._get_lot(strategy)

        history.open_bars = strategy.open_bars
        history.shut_bars = strategy.shut_bars
        history.takes = strategy.takes
        history.stops = strategy.stops

        history.close_bars = strategy.close_bars

        history.durations = strategy.durations
        history.open_prices = strategy.open_prices
        history.close_prices = strategy.close_prices
        history.gains = strategy.gains

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return history

    @staticmethod
    def _get_trade_index(strategy):
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

    @staticmethod
    def _get_order_index(strategy):
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

    @staticmethod
    def _get_asset_id(strategy):
        """
        Return asset id of each order.

        Returns
        -------
        asset_id : array, shape (n_orders, )

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

    @staticmethod
    def _get_asset(strategy):
        return strategy.universe.assets[strategy.asset_id]

    @staticmethod
    def _get_lot(strategy):
        """
        Return lot of each order.

        Returns
        -------
        lot : array, shape (n_orders, )

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

    # TODO
    # @staticmethod
    # def _get_open_bar_id(strategy):
    #     """
    #     Return open_bar of each trade/order.

    #     Parameters
    #     ----------
    #     - strategy
    #     - columns : {'trades', 'orders'}, default 'trades'

    #     Returns
    #     -------
    #     If columns = 'trades' :
    #         open_bar_ids : array, shape (n_trades, )
    #     If columns = 'orders' :
    #         open_bar_ids : array, shape (n_orders, )

    #     Examples
    #     --------
    #     >>> strategy.universe.bars
    #     Index(['01-01', '01-02', '01-03', ...])
    #     >>> strategy.trades = [
    #     ...     Trade(open_bar='01-01', asset=['Asset0', 'Asset1'], ...),
    #     ...     Trade(open_bar='01-02', asset=['Asset2'], ...),
    #     ... ]
    #     >>> strategy.open_bar_ids
    #     array([ 1, 2])
    #     """
    #     if columns == 'orders':
    #         return np.repeat(
    #             open_bar_ids(strategy, columns='trades'),
    #             [trade.n_orders for trade in strategy.trades],
    #         )

    #     def ifnonefirst(bar):
    #         if bar is None:
    #             return strategy.universe.bars[0]
    #         else:
    #             return bar
    #     open_bars = [ifnonefirst(trade.open_bar) for trade in strategy.trades]
    #     return strategy.universe._bar_id(open_bars)
