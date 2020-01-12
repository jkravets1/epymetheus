import pandas as pd


class Wealth:
    """
    Represent time-series of wealth.
    """
    def __init__(self, data, bars):
        self.data = data
        self.bars = bars

    @classmethod
    def _from_backtester(cls, backtester):
        if not hasattr(backtester, 'transaction_'):
            raise ValueError

        transaction = backtester.transaction_.to_frame()
        position = transaction.cumsum().shift().fillna(0.0)
        prices = backtester.universe.data

        data = (position * prices.diff()).sum(axis=1).cumsum()

        return cls(data=data, bars=backtester.universe.bars)

    def to_series(self):
        return pd.Series(data=self.data, index=self.bars)
