import pandas as pd

from ._bunch import Bunch

# Bunch? pd.Series?

class Wealth(Bunch):  # Bunch?
    """
    Represent time-series of wealth.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _from_strategy(cls, strategy):
        transaction = strategy.transaction.to_frame()
        position = transaction.cumsum().shift().fillna(0.0)
        prices = strategy.universe.data

        wealth = (position * prices.diff()).sum(axis=1).cumsum()

        return cls(wealth=wealth)

    # def to_series(self):
    #     return pd.Series(data=self.data, index=self.bars)
