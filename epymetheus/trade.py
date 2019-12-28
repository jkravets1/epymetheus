import pandas as pd
from functools import reduce
from copy import copy

from datetime import timedelta

class Trade():
    """
    Represent a single trade.

    Paramters
    ---------
    - asset : str
        Name of asset.
    - lot : float
        Lot to trade in unit of share.
    - begin_date : datetime.date
        Date to open the trade.
    - end_date : datetime.date
        Date to close the trade.

    Example
    -------
    A long position of AAPL is given by:

    >>> bd = datetime.date(2018, 1, 1)
    >>> ed = datetime.date(2018, 2, 1)
    >>> trade = Trade(
    ...     asset='AAPL', lot=123.4,
    ...     begin_date=bd, end_date=ed
    ... )

    One can also make a short position.  In unit of price,

    >>> trade = Trade(
    ...     asset='AAPL', lot=-45.6,
    ...     begin_date=bd, end_date=ed
    ... )
    """
    def __init__(self, asset, lot, begin_date, end_date):
        self.asset = asset
        self.lot = lot
        self.begin_date = begin_date
        self.end_date = end_date

    def __mul__(self, num):
        trade = copy(self)
        trade.lot *= num
        return trade

    def __rmul__(self, num):
        return self.__mul__(num)

    def __neg__(self):
        return self.__mul__(-1)

    def shift(self, delta):
        """
        Return trade of which begin_date and end_date are shifted.
        """
        if isinstance(delta, int):
            delta = timedelta(days=delta)
        trade = copy(self)
        trade.begin_date += delta
        trade.end_date += delta
        return trade

    def __str__(self):
        return (
            f'Trade: {self.asset} * {self.lot}'
            f' {self.begin_date} - {self.end_date}'
        )


class TradeHistory:

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_trades(cls, trades, universe):
        """
        Transform Iterable of trades into dataframe.

        Examples
        --------
        >>> trades = [Trade(...), ...]
        >>> TradeHistory(trades).data
          asset  lot  begin_date    end_date duration gain
        0  AAPL 10.0  2000-01-01  2000-01-31       30  123
        1  MSFT 12.0  2000-03-01  2000-03-12       11  456
        ...
        """
        data = pd.DataFrame({
            attr: getattr(trade, attr)
            for attr in ('asset', 'lot', 'begin_date', 'end_date')
        } for trade in trades)

        data['duration'] = cls.__duration(data)
        data['gain'] = cls.__gain(data, universe)

        return cls(data=data)

    @staticmethod
    def __duration(data):
        return data['end_date'] - data['begin_date']

    @staticmethod
    def __gain(data, universe):
        bdprice = pd.Series(
            universe.data.at[row.begin_date, row.asset]
            for row in data.itertuples()
        )
        edprice = pd.Series(
            universe.data.at[row.end_date, row.asset]
            for row in data.itertuples()
        )
        return data['lot'] * (edprice - bdprice)


class Transaction:
    # transaction is sparser and lighter than position
    # TODO is name appropriate?
    # TODO numpy sparse matrix
    # TODO one-day delay?

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_trades(cls, trades, universe):
        """
        Return transaction as pandas.DataFrame, in unit of share.

        Notes
        -----
        It is faster to make buysell first and cumsum it.
        """
        def trade_to_tr(trade):
            return trade.lot * pd.DataFrame(
                {trade.asset: [1.0, -1.0]},
                index=[trade.begin_date, trade.end_date]
            )

        def sum_fillz(dfs):
            add_fillz = lambda df1, df2: df1.add(df2, fill_value=0.0)
            return reduce(add_fillz, dfs).fillna(0.0)

        data = sum_fillz(map(trade_to_tr, trades))
        return cls(data=data)


class Wealth:

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_transaction(cls, transaction, universe):
        position = transaction.data.shift().cumsum()
        data = (position * universe.data.diff()).sum(axis=1).cumsum()
        return cls(data=data)
