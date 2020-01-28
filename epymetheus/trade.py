from copy import copy

import numpy as np

from .utils import Bunch

try:
    from functools import cached_property
except ImportError:
    cached_property = property


class Trade:
    """
    Represent a single trade.

    Paramters
    ---------
    - asset : str
        Name of asset.
    - open_bar
        Bar to open the trade.
    - close_bar
        Bar to close the trade.
    - lot : float, default 1.0
        Lot to trade in unit of share.

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
    ...     asset='AAPL', lot=123.4, open_bar=od, close_bar=cd,
    ... )

    Short position:
    >>> trade = -45.6 * Trade(
    ...     asset='AAPL', open_bar=od, close_bar=cd,
    ... )

    Long-short position:
    >>> trade = Trade(
    ...     asset=['AAPL', 'MSFT'],
    ...     lot=[12.3, -45.6],
    ...     open_bar=od,
    ...     close_bar=cd,
    ... )
    """
    def __init__(self, asset, open_bar, close_bar, lot=1.0):
        self.asset = asset
        self.open_bar = open_bar
        self.close_bar = close_bar
        self.lot = lot

    @property
    def n_orders(self):
        if hasattr(self.lot, '__iter__'):
            return len(self.lot)
        else:
            return 1

    @cached_property
    def as_array(self):
        return Bunch(
            asset=np.array(self.asset).reshape(-1),
            lot=np.array(self.lot).reshape(-1),
            open_bar=np.tile(np.array(self.open_bar), self.n_orders),
            close_bar=np.tile(np.array(self.close_bar), self.n_orders),
        )

    def __mul__(self, num):
        trade = copy(self)
        if hasattr(self.lot, '__iter__'):
            trade.lot = [lot * num for lot in trade.lot]
        else:
            trade.lot *= num
        return trade

    def __rmul__(self, num):
        return self.__mul__(num)

    def __neg__(self):
        return self.__mul__(-1.0)

    def __truediv__(self, num):
        print(1.0 / num)
        return self.__mul__(1.0 / num)

    def __floordiv__(self, num):
        trade = copy(self)
        if hasattr(self.lot, '__iter__'):
            trade.lot = [lot // num for lot in trade.lot]
        else:
            trade.lot //= num
        return trade
