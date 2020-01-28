import numpy as np
import pandas as pd

from .utils import Bunch


class Wealth(Bunch):
    """
    Represent time-series of wealth.

    Attributes
    ----------
    - wealth
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _from_strategy(cls, strategy):
        transaction = pd.DataFrame(strategy.transaction).set_index('bars')
        position = transaction.cumsum(axis=0).shift().fillna(0.0).values
        prices = strategy.universe.prices.values
        price_changes = np.diff(prices, axis=0, prepend=0.0)

        wealth = (position * price_changes).sum(axis=1).cumsum()
        return cls(bars=strategy.universe.bars, wealth=wealth)

    # @property
    # def n_bars(self):
    #     return len(self.wealth)

    # def to_series(self):
    #     return pd.Series(data=self.data, index=self.bars)
