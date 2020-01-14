import numpy as np

from .utils import Bunch


class History(Bunch):
    """
    Attributes
    ----------
    - assets
    - lots
    - open_dates
    - close_dates
    - durations
    - open_prices
    - gains

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
        trades = np.array(list(strategy.logic(
            strategy.universe, **strategy.params
        )))

        index = np.concatenate([
            np.repeat(i, trade.n_bets)
            for i, trade in enumerate(trades)
        ])

        # TODO avoid comprehension notation
        history = cls(
            index=index,
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

        # TODO can be rewritten using np.vectorize.
        history.open_prices = history.__open_prices(strategy.universe)
        history.gains = history.__gains(strategy.universe)

        return history

    def __open_prices(self, universe):
        def get_price(date, asset):
            return universe.prices.at[date, asset]

        get_prices = np.frompyfunc(get_price, 2, 1)

        return get_prices(self.open_dates, self.assets)

    def __gains(self, universe):
        def get_price(date, asset):
            return universe.prices.at[date, asset]

        get_prices = np.frompyfunc(get_price, 2, 1)

        open_prices = get_prices(self.open_dates, self.assets)
        close_prices = get_prices(self.close_dates, self.assets)

        return (close_prices - open_prices) * self.lots
