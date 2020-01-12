from operator import attrgetter

import numpy as np

from ._bunch import Bunch


class TradeHistory(Bunch):
    """

    Attributes
    ----------
    - assets
    - lots
    - open_dates
    - close_dates
    - durations
    - gains

    Examples
    --------
    >>> history = ...
    >>> history.asset
    ['AAPL', 'MSFT', ...]
    >>> history
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def _from_backtester(cls, backtester):
        """
        Initialize self from backtester.
        """
        if not hasattr(backtester, 'strategy'):
            raise ValueError
        if not hasattr(backtester, 'universe'):
            raise ValueError

        trades = np.array(list(backtester.strategy.logic(
            backtester.universe, **backtester.strategy.params
        )))

        history = cls(
            assets=np.vectorize(attrgetter('asset'))(trades),
            lots=np.vectorize(attrgetter('lot'))(trades),
            open_dates=np.vectorize(attrgetter('open_date'))(trades),
            close_dates=np.vectorize(attrgetter('close_date'))(trades),
        )

        history.durations = history.close_dates - history.open_dates

        # TODO can be rewritten using np.vectorize.
        history.open_prices = history.__open_prices(backtester.universe)
        history.gains = history.__gains(backtester.universe)

        return history

    def __open_prices(self, universe):
        def get_price(date, asset):
            return universe.data.at[date, asset]

        get_prices = np.frompyfunc(get_price, 2, 1)

        return get_prices(self.open_dates, self.assets)

    def __gains(self, universe):
        def get_price(date, asset):
            return universe.data.at[date, asset]

        get_prices = np.frompyfunc(get_price, 2, 1)

        open_prices = get_prices(self.open_dates, self.assets)
        close_prices = get_prices(self.close_dates, self.assets)

        return (close_prices - open_prices) * self.lots
