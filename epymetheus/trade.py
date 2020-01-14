from copy import copy
from datetime import timedelta


class Trade:
    """
    Represent a single trade.

    Paramters
    ---------
    - asset : str
        Name of asset.
    - lot : float
        Lot to trade in unit of share.
    - open_date : datetime.date
        Date to open the trade.
    - close_date : datetime.date
        Date to close the trade.

    Example
    -------
    A long position of AAPL is given by:

    >>> od = datetime.date(2018, 1, 1)
    >>> cd = datetime.date(2018, 2, 1)
    >>> trade = Trade(
    ...     asset='AAPL', lot=123.4,
    ...     open_date=od, close_date=cd,
    ... )

    One can also make a short position.  In unit of price,

    >>> trade = Trade(
    ...     asset='AAPL', lot=-45.6,
    ...     open_date=od, close_date=cd,
    ... )
    """
    def __init__(self, asset, lot, open_date, close_date):
        self.asset = asset
        self.lot = lot
        self.open_date = open_date
        self.close_date = close_date

    def __mul__(self, num):
        trade = copy(self)
        trade.lot *= num
        return trade

    def __rmul__(self, num):
        return self.__mul__(num)

    def __neg__(self):
        return self.__mul__(-1.0)

    def shift(self, delta):
        """
        Return trade of which begin_date and end_date are shifted.
        """
        if isinstance(delta, int):
            delta = timedelta(days=delta)
        trade = copy(self)
        trade.open_date += delta
        trade.close_date += delta
        return trade

    # def __str__(self):
    #     return (
    #         f'Trade: {self.asset} * {self.lot}'
    #         f' {self.open_date} - {self.close_date}'
    #     )
