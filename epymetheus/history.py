from time import time

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
        history.trade_index = strategy.trade_index
        history.order_index = strategy.order_index
        history.assets = strategy.assets
        history.lots = strategy.lots
        history.open_bars = strategy.open_bars
        history.shut_bars = strategy.shut_bars
        history.atakes = strategy.atakes
        history.acuts = strategy.acuts

        history.close_bars = strategy.close_bars

        history.durations = strategy.durations
        history.open_prices = strategy.open_prices
        history.close_prices = strategy.close_prices
        history.gains = strategy.gains

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return history
