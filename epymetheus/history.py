from time import time

import numpy as np

from epymetheus.utils import Bunch
from epymetheus.utils.array import catch_first, cross_up


class History(Bunch):
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
    def __init__(self, strategy=None, verbose=True, **kwargs):
        if strategy is not None:
            history = self.__from_strategy(strategy, verbose=verbose)
            super().__init__(**history)
        else:
            super().__init__(**kwargs)

    @classmethod
    def __from_strategy(cls, strategy, verbose=True):
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
        begin_time = time()

        if verbose:
            print('Evaluating history ... ', end='')

        if strategy.n_trades == 0:
            return cls._empty()

        history = cls()

        history.trade_index = strategy.trade_index
        history.order_index = strategy.order_index
        history.assets = strategy.assets
        history.lots = strategy.lots
        history.open_bars = strategy.open_bars
        history.close_bars = strategy.close_bars

        # TODO
        # history._get_close_bars(strategy)

        # history.durations = history._get_durations(strategy)
        # history.open_prices = history._get_open_prices(strategy)
        # history.close_prices = history._get_close_prices(strategy)
        # history.gains = history._get_gains(strategy)
        history.durations = strategy.durations
        history.open_prices = strategy.open_prices
        history.close_prices = strategy.close_prices
        history.gains = strategy.gains

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return history

    def _get_durations(self, strategy=None):
        """
        Return durations of orders.

        Parameters
        ----------
        - strategy : TradeStrategy
            Ignored.

        Returns
        -------
        durations : array, shape (n_orders, )
            Duration of each trade.
        """
        return self.close_bars - self.open_bars

    def _get_open_prices(self, strategy):
        """
        Return open_prices of orders.

        Parameters
        ----------
        - strategy : TradeStrategy
            Trade strategy with the following attributes:
            * universe

        Returns
        -------
        open_prices : array, shape (n_orders, )
            Price at open_bar for each order.
        """
        return strategy.universe._pick_prices(self.open_bars, self.assets)

    def _get_close_prices(self, strategy):
        """
        Return open_prices of orders.

        Parameters
        ----------
        - strategy : TradeStrategy
            Trade strategy with the following attributes:
            * universe

        Returns
        -------
        close_prices : array, shape (n_orders, )
            Price at close_bar for each order.
        """
        return strategy.universe._pick_prices(self.close_bars, self.assets)

    def _get_gains(self, strategy=None):
        """
        Return gains of orders.

        Parameters
        ----------
        - strategy : TradeStrategy
            Ignored.

        Returns
        -------
        gains : array, shape (n_orders, )
            Gain of each order.
        """
        gains = (self.close_prices - self.open_prices) * self.lots
        return gains

    def _get_close_bars(self, strategy):
        """
        Get close bars based on atakes.

        Returns
        -------
        close_bars : shape (n_trades, )
            Represent close bar of each trade.
        """
        acumpnl = strategy._acumpnl_matrix
        atakes = [trade.atake or np.inf for trade in strategy.trades]

        return catch_first(np.logical_or.reduce([
            strategy._closebar_matrix,
            cross_up(acumpnl, threshold=atakes),
        ]))

    @classmethod
    def _empty(cls):
        """
        Return empty history.

        Returns
        -------
        empty_history : History
        """
        return cls(
            index=np.zeros((0)),
            assets=np.array([], dtype=str),
            lots=np.zeros((0)),
            open_bars=np.zeros((0)),
            close_bars=np.zeros((0)),
            open_prices=np.zeros((0)),
            close_prices=np.zeros((0)),
            gains=np.zeros((0)),
        )
