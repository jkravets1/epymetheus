from functools import reduce

import numpy as np
import pandas as pd

from ._bunch import Bunch


class Transaction(Bunch):
    """
    Represent transaction history.

    Examples
    --------
    >>> transaction
    {'AAPL': np.array([1.0,  0.0, -1.0, ...],
     'MSFT': np.array([2.0, -2.0,  0.0, ...], ... }
    >>> transaction.bars
    np.array(['2000-01-01', ...])
    >>> transaction.assets
    np.array(['AAPL', 'MSFT', ...])

    >>> transaction.to_frame()  # pandas.DataFrame
               AAPL MSFT ....
    2000-01-01  1.0  2.0 ....
    2000-01-02  0.0 -2.0 ....
    2000-01-03 -1.0  0.0 ....
    .......... .... .... ....
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _from_strategy(cls, strategy):
        """
        Initialize self from strategy.
        """
        def to_series(lot, open_date, close_date):
            """
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
            def add_fillzero(s1, s2):
                return s1.add(s2, fill_value=0.0)
            return reduce(add_fillzero, list_series)

        def to_data(asset):
            idx = (strategy.history.assets == asset)

            lots = strategy.history.lots[idx]
            open_dates = strategy.history.open_dates[idx]
            close_dates = strategy.history.close_dates[idx]

            list_series = np.frompyfunc(to_series, 3, 1)(
                lots, open_dates, close_dates
            )
            return sum_fillzero(list_series)

        assets = strategy.universe.assets
        data = {asset: to_data(asset) for asset in assets}

        transaction = cls()
        for key, value in data.items():
            setattr(transaction, key, value)

        return transaction

    def to_frame(self):
        return pd.DataFrame(
            data=self.data, index=self.bars, columns=self.assets
        ).fillna(0.0)
