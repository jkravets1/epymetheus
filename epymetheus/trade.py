from copy import deepcopy

import numpy as np

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
    - open_bar : object
        Bar to open the trade.
    - close_bar : object or None, default None
        Bar to close the trade.
    - lot : float, default 1.0
        Lot to trade in unit of share.
    - atake : float > 0 or None, default None
    - rtake : float > 0 or None, default None
    - acut : float < 0 or None, default None
    - rcut : float < 0 or None, default None

    Attributes
    ----------
    - n_orders : int
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
    def __init__(
        self,
        asset,
        open_bar,
        close_bar=None,
        lot=1.0,
        atake=None,
        rtake=None,
        acut=None,
        rcut=None,
    ):
        self.asset = np.array(asset).reshape(-1)
        self.open_bar = open_bar
        self.close_bar = close_bar
        self.lot = np.array(lot, dtype=np.float64).reshape(-1)
        self.atake = atake
        self.rtake = rtake
        self.acut = acut
        self.rcut = rcut

    @property
    def n_orders(self):
        if hasattr(self.lot, '__iter__'):
            return len(self.lot)
        else:
            return 1

    # @cached_property
    # def _as_array(self):
    #     return Bunch(
    #         asset=np.array(self.asset).reshape(-1),
    #         lot=np.array(self.lot).reshape(-1),
    #         open_bar=np.tile(np.array(self.open_bar), self.n_orders),
    #         close_bar=np.tile(np.array(self.close_bar), self.n_orders),
    #         atake=np.tile(np.array(self.atake), self.n_orders),
    #     )

    def _lot_vector(self, universe):
        """
        Return 1d array of lot to trade each asset.

        Returns
        -------
        lot_vector : array, shape (n_assets, )

        Examples
        --------
        >>> universe.assets
        Index(['AAPL', 'MSFT', 'AMZN'], dtype='object')
        >>> trade = Trade(['AAPL', 'MSFT'], lot=[1, -2], ...)
        >>> trade._lot_vector(universe)
        array([1, -2,  0])
        """
        asset_onehot = universe._asset_onehot(self.asset)
        return np.dot(self.lot, asset_onehot)

    def __eq__(self, other):
        return (
            (self.asset == other.asset).all() and
            self.open_bar == other.open_bar and
            (self.lot == other.lot).all() and
            self.atake == other.atake and
            self.rtake == other.rtake and
            self.acut == other.acut and
            self.rcut == other.rcut
        )

    def __mul__(self, num):
        """
        Multiply lot of self.

        Examples
        --------
        >>> trade = -2.0 * Trade(..., lot=1.2)
        >>> trade.lot
        -2.4
        """
        trade = deepcopy(self)
        trade.lot *= num
        # if hasattr(self.lot, '__iter__'):
        #     trade.lot = np.array([lot * num for lot in trade.lot])
        # else:
        #     trade.lot *= num
        return trade

    def __rmul__(self, num):
        return self.__mul__(num)

    def __neg__(self):
        return self.__mul__(-1.0)

    def __truediv__(self, num):
        print(1.0 / num)
        return self.__mul__(1.0 / num)

    # def __floordiv__(self, num):
    #     trade = deepcopy(self)
    #     if hasattr(self.lot, '__iter__'):
    #         trade.lot = np.array([lot // num for lot in trade.lot])
    #     else:
    #         trade.lot //= num
    #     return trade
