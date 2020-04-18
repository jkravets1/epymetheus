from functools import reduce

import numpy as np
import pandas as pd

from epymetheus.utils import TradeResult


class Wealth(TradeResult):
    """
    Represent time-series of wealth.

    Attributes
    ----------
    - bars : numpy.array, shape (n_bars, )
        Bar of universe.
    - wealth : numpy.array, shape (n_bars, )
        Time-series of wealth.
    """
    @classmethod
    def from_strategy(cls, strategy):
        """
        Initialize wealth from strategy.

        Parameters
        ----------
        - strategy : TradeStrategy
        - verbose : bool
        """
        return cls(
            bars=cls._get_bars(strategy),
            wealth=cls._get_wealth(strategy),
        )

    @staticmethod
    def _get_bars(strategy):
        return strategy.universe.bars

    @staticmethod
    def _get_wealth(strategy):
        return reduce(np.add, (
            trade.series_pnl(strategy.universe)
            for trade in strategy.trades
        ))

    def to_series(self, name='wealth', copy=False):
        """
        Represent self as `pandas.Series`.

        Parameters
        ----------
        - name : str, default 'wealth'
            The name to give to the Series.
        - copy : bool, default False
            Copy input data.

        Returns
        -------
        series_wealth : pandas.Series
        """
        return pd.Series(self.wealth, index=self.bars, name=name, copy=copy)

    def to_dataframe(self, copy=False):
        """
        Represent self as `pandas.DataFrame`.

        Parameters
        ----------
        - copy : bool, default False
            Copy input data.

        Returns
        -------
        df_wealth : pandas.DataFrame
        """
        return pd.DataFrame(self, copy=copy).set_index('bars')
