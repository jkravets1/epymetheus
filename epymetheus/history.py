from time import time

import numpy as np

from epymetheus.utils import Bunch


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
            super().__init__(**self.__from_strategy(strategy, verbose=verbose))
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
            return cls.__empty()

        history = cls()

        history.trade_index = strategy.trade_index
        history.order_index = strategy.order_index
        history.assets = strategy.assets
        history.lots = strategy.lots
        history.open_bars = strategy.open_bars
        history.close_bars = strategy.close_bars

        # TODO
        # history._get_close_bars(strategy)

        history.durations = strategy.durations
        history.open_prices = strategy.open_prices
        history.close_prices = strategy.close_prices
        history.gains = strategy.gains

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return history

    @classmethod
    def __empty(cls):
        """
        Return empty history.

        Returns
        -------
        empty_history : History
        """
        return cls(
            trade_index=np.zeros((0)),
            order_index=np.zeros((0)),
            assets=np.array([], dtype=str),
            lots=np.zeros((0)),
            open_bars=np.zeros((0)),
            close_bars=np.zeros((0)),
            durations=np.zeros((0)),
            open_prices=np.zeros((0)),
            close_prices=np.zeros((0)),
            gains=np.zeros((0)),
        )
