from copy import copy
from datetime import timedelta

import numpy as np

from .utils import Bunch


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

    Attributes
    ----------
    - n_bets : int
        Number of assets to bet.

    Example
    -------
    Long position:
    >>> od = datetime.date(2018, 1, 1)
    >>> cd = datetime.date(2018, 2, 1)
    >>> trade = Trade(
    ...     asset='AAPL', lot=123.4,
    ...     open_date=od, close_date=cd,
    ... )

    Short position:
    >>> trade = Trade(
    ...     asset='AAPL', lot=-45.6,
    ...     open_date=od, close_date=cd,
    ... )

    Long-short position:
    >>> trade = Trade(
    ...     asset=['AAPL', 'MSFT'],
    ...     lot=[12.3, -45.6],
    ...     open_date=od, close_date=cd,
    ... )

    Data are stored as `numpy.array` (even if one is betting on a single asset):
    >>> trade.asset
    array(['AAPL', 'MSFT'])
    >>> trade.lot
    array([12.3, -45.6])
    >>> trade.open_date
    array(['2018-01-01', '2018-01-01'])
    >>> trade.close_date
    array(['2018-01-01', '2018-01-01'])
    """
    def __init__(self, asset, lot, open_date, close_date):
        self.asset = asset
        self.lot = lot
        self.open_date = open_date
        self.close_date = close_date

        self.n_bets = np.array(self.asset).size

        self._as_array = Bunch(
            asset=np.array(self.asset).reshape(-1),
            lot=np.array(self.lot).reshape(-1),
            open_date=np.tile(np.array(self.open_date), self.n_bets),
            close_date=np.tile(np.array(self.close_date), self.n_bets),
        )

    def __mul__(self, num):
        trade = copy(self)
        trade.lot *= num
        return trade

    def __rmul__(self, num):
        return self.__mul__(num)

    def __neg__(self):
        return self.__mul__(-1.0)

    @property
    def as_array(self):
        return self._as_array

    # def shift(self, delta):
    #     """
    #     Return trade of which begin_date and end_date are shifted.
    #     """
    #     if isinstance(delta, int):
    #         delta = timedelta(days=delta)
    #     trade = copy(self)
    #     trade.open_date += delta
    #     trade.close_date += delta
    #     return trade
