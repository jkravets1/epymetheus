from time import time

import numpy as np

from epymetheus.exceptions import NotRunError
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
        if not strategy.is_run:
            raise NotRunError('Strategy has not been run')

        if verbose:
            msg = 'Evaluating history'
            print(f'{msg:<22} ... ', end='')
            begin_time = time()

        history = cls(
            trade_index=cls._get_trade_index(strategy),
            order_index=cls._get_order_index(strategy),
            asset=cls._get_asset(strategy),
            lot=cls._get_lot(strategy),
            open_bar=cls._get_open_bar(strategy),
            close_bar=cls._get_close_bar(strategy),
            shut_bar=cls._get_shut_bar(strategy),
            take=cls._get_take(strategy),
            stop=cls._stop(strategy),
            # gain=cls._get_gain(strategy),
        )

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
    def _get_asset(strategy):
        return np.concatenate([
            trade.array_asset for trade in strategy.trades
        ])

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
            trade.array_lot for trade in strategy.trades
        ])

    def _get_open_bar(strategy):
        return np.repeat(
            np.arange(strategy.n_trades),
            [trade.open_bar for trade in strategy.trades]
        )

    def _get_close_bar(strategy):
        return np.repeat(
            np.arange(strategy.n_trades),
            [trade.close_bar for trade in strategy.trades]
        )

    def _get_shut_bar(strategy):
        return np.repeat(
            np.arange(strategy.n_trades),
            [trade.close_bar for trade in strategy.trades]
        )

    def _get_take(strategy):
        return np.repeat(
            np.arange(strategy.n_trades),
            [trade.take for trade in strategy.trades]
        )

    def _get_stop(strategy):
        return np.repeat(
            np.arange(strategy.n_trades),
            [trade.stop for trade in strategy.trades]
        )

    # def _get_gain(strategy):
    #     return
