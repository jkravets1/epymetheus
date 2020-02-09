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
    - open_bar : object or None, default None
        Bar to open the trade.
    - shut_bar : object or None, default None
        Bar to enforce the trade to close.
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
    ...     asset='AAPL', lot=123.4, open_bar=od, shut_bar=cd,
    ... )

    Short position:
    >>> trade = -45.6 * Trade(
    ...     asset='AAPL', open_bar=od, shut_bar=cd,
    ... )

    Long-short position:
    >>> trade = Trade(
    ...     asset=['AAPL', 'MSFT'],
    ...     lot=[12.3, -45.6],
    ...     open_bar=od,
    ...     shut_bar=cd,
    ... )
    """
    def __init__(
        self,
        asset,
        open_bar=None,
        shut_bar=None,
        lot=1.0,
        atake=None,
        rtake=None,
        acut=None,
        rcut=None,
    ):
        self.asset = np.array(asset).reshape(-1)
        self.open_bar = open_bar
        self.shut_bar = shut_bar
        self.lot = np.array(lot, dtype=np.float64).reshape(-1)
        self.atake = atake
        self.rtake = rtake
        self.acut = acut
        self.rcut = rcut

        self.__check_params()

    @property
    def n_orders(self):
        return self.lot.size

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
        asset_id = universe.assets.get_indexer(self.asset)
        asset_onehot = universe._asset_onehot(asset_id)
        return np.dot(self.lot, asset_onehot)

    def __check_params(self):
        if self.asset.size != self.lot.size:
            raise ValueError('Numbers of asset and lot should be equal')

    def __eq__(self, other):
        return all([
            (self.asset == other.asset).all(),
            self.open_bar == other.open_bar,
            (self.lot == other.lot).all(),
            self.atake == other.atake,
            self.rtake == other.rtake,
            self.acut == other.acut,
            self.rcut == other.rcut,
        ])

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
        return trade

    def __rmul__(self, num):
        return self.__mul__(num)

    def __neg__(self):
        return self.__mul__(-1.0)

    def __truediv__(self, num):
        return self.__mul__(1.0 / num)
