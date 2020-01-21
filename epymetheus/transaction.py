from functools import reduce

import numpy as np
import pandas as pd

from .utils import Bunch


class Transaction(Bunch):
    """
    Represent transaction history.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _from_strategy(cls, strategy):
        """Initialize self from strategy."""
        def to_transaction(lot, open_date, close_date):
            """
            Return transaction of single trade as pandas.Series.

            Examples
            --------
            >>> lot = 2.0
            >>> open_date, close_date = '2000-01-01', '2000-01-05'
            >>> to_series(lot, open_date, close_date)
            2000-01-01  2.0
            2000-01-05 -2.0
            """
            return lot * pd.Series(
                [1.0, -1.0], index=[open_date, close_date]
            )

        def sum_fillzero(list_series):
            """Sum Series by filling 0."""
            def add_fillzero(s1, s2):
                return s1.add(s2, fill_value=0.0)
            return reduce(add_fillzero, list_series, pd.Series())

        def to_data(asset):  # TODO rename clearly
            """Return transaction of an asset."""
            idx = (strategy.history.assets == asset)

            lots = strategy.history.lots[idx]
            open_bars = strategy.history.open_bars[idx]
            close_bars = strategy.history.close_bars[idx]

            list_series = np.frompyfunc(to_transaction, 3, 1)(
                lots, open_bars, close_bars
            )
            data = sum_fillzero(list_series)
            data = data.reindex(strategy.universe.bars, fill_value=0.0)
            return data.values

        assets = strategy.universe.assets
        data = {asset: to_data(asset) for asset in assets}

        transaction = cls(bars=strategy.universe.bars)
        for key, value in data.items():
            setattr(transaction, key, value)

        return transaction

    # def to_frame(self):
    #     return pd.DataFrame(self)
