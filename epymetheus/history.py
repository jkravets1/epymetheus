import numpy as np

from .utils import Bunch


class History(Bunch):
    """
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
    - open_dates : numpy.array, shape (n_orders, )
    - close_dates : numpy.array, shape (n_orders, )
    - durations : numpy.array, shape (n_orders, )
    - open_prices : numpy.array, shape (n_orders, )
    - close_prices : numpy.array, shape (n_orders, )
    - gains : numpy.array, shape (n_orders, )

    Examples
    --------
    >>> history.assets
    array(['AAPL', 'MSFT', ...])
    >>> history.lots
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _from_strategy(cls, strategy):
        """
        Initialize self from strategy.
        """
        # Generator or iterator of trades
        gen_trades = strategy.logic(strategy.universe, **strategy.params)

        if gen_trades is None:  # If no trade has been yielded
            return cls(
                index=np.array([]),
                assets=np.array([], dtype=str),
                lots=np.array([]),
                open_dates=np.array([]),
                close_dates=np.array([]),
                open_prices=np.array([]),
                close_prices=np.array([]),
                gains=np.array([]),
            )

        trades = np.array(list(gen_trades))

        trade_index = np.concatenate([
            np.repeat(i, trade.n_bets) for i, trade in enumerate(trades)
        ])
        order_index = np.arange(len(trade_index))

        # TODO not beautiful; avoid comprehension notation
        history = cls(
            order_index=order_index,
            trade_index=trade_index,
            assets=np.concatenate([
                trade.as_array.asset for trade in trades]),
            lots=np.concatenate([
                trade.as_array.lot for trade in trades]),
            open_dates=np.concatenate([
                trade.as_array.open_date for trade in trades]),
            close_dates=np.concatenate([
                trade.as_array.close_date for trade in trades]),
        )

        history.durations = history.close_dates - history.open_dates
        history.open_prices = history._get_open_prices(strategy.universe)
        history.close_prices = history._get_close_prices(strategy.universe)
        history.gains = history._get_gains()

        return history

    def _pick_prices(self, universe, dates, assets):
        """
        Pick array of prices of given dates (array-like) and
        assets (array-like) from universe.
        """
        def pick_price(date, asset):
            return universe.prices.at[date, asset]
        return np.frompyfunc(pick_price, 2, 1)(dates, assets)

    def _get_open_prices(self, universe):
        return self._pick_prices(universe, self.open_dates, self.assets)

    def _get_close_prices(self, universe):
        return self._pick_prices(universe, self.close_dates, self.assets)

    def _get_gains(self):
        return (self.close_prices - self.open_prices) * self.lots
