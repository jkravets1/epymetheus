from copy import deepcopy

import numpy as np


class Trade:
    """
    Represent a single trade.

    Parameters
    ----------
    - asset : str or array of str
        Name of assets.
    - open_bar : object or None, default None
        Bar to open the trade.
    - shut_bar : object or None, default None
        Bar to enforce the trade to close.
    - lot : float, default 1.0
        Lot to trade in unit of share.
    - take : float > 0 or None, default None
        Threshold of profit-take.
    - stop : float < 0 or None, default None
        Threshold of stop-loss.

    Examples
    --------
    A long position:
    >>> od = datetime.date(2018, 1, 1)
    >>> cd = datetime.date(2018, 2, 1)
    >>> trade = Trade(
    ...     asset='AAPL',
    ...     lot=123.4,
    ...     open_bar=od,
    ...     shut_bar=cd,
    ... )

    A short position:
    >>> trade = -45.6 * Trade(
    ...     asset='AAPL',
    ...     open_bar=od,
    ...     shut_bar=cd,
    ... )

    A long-short position:
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
        lot=1.0,
        open_bar=None,
        shut_bar=None,
        take=None,
        stop=None,
    ):
        self.asset = asset
        self.lot = lot
        self.open_bar = open_bar
        self.shut_bar = shut_bar
        self.take = take
        self.stop = stop

    # def __check_params(self):
    #     if self.asset.size != self.lot.size:
    #         raise ValueError('Numbers of asset and lot should be equal')

    @property
    def _array_asset(self):
        """
        Return asset as `numpy.array`.

        Returns
        -------
        array_asset : numpy.array, shape (n_orders, )

        Examples
        --------
        >>> trade = Trade(asset='AAPL', ...)
        >>> trade.a_asset
        array(['AAPL'])

        >>> trade = Trade(asset=['AAPL', 'MSFT'])
        >>> trade.a_asset
        array(['AAPL', 'MSFT'])
        """
        return np.array(self.asset).reshape(-1)

    @property
    def _array_lot(self):
        """
        Return lot as `numpy.array`.

        Returns
        -------
        array_lot : numpy.array, shape (n_orders, )

        Examples
        --------
        >>> trade = Trade(lot=1.2, ...)
        >>> trade.a_lot
        array([1.2])

        >>> trade = Trade(asset=[1.2, 3.4])
        >>> trade.a_asset
        array([1.2, 3.4])
        """
        return np.array(self.lot).reshape(-1)

    @property
    def _n_orders(self):
        return self._array_lot.size

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

    # def __eq__(self, other):
    #     return all([
    #         (self.array_asset == other.array_asset).all(),
    #         self.open_bar == other.open_bar,
    #         (self.array_lot == other.array_lot).all(),
    #         self.take == other.take,
    #         self.stop == other.stop,
    #     ])

    def __mul__(self, num):
        """
        Multiply lot of self.

        Examples
        --------
        >>> trade = -2.0 * Trade(..., lot=1.2)
        >>> trade.lot
        -2.4
        """
        self.lot = num * self._array_lot
        return self

    def __rmul__(self, num):
        """
        Multiply lot of self.

        Examples
        --------
        >>> trade = Trade(..., lot=1.2) * (-2.0)
        >>> trade.lot
        -2.4
        """
        return self.__mul__(num)

    def __neg__(self):
        """
        Invert the lot of self.

        Examples
        --------
        >>> trade = -Trade(..., lot=1.2)
        >>> trade.lot
        -1.2
        """
        return self.__mul__(-1.0)

    def __truediv__(self, num):
        """
        Divide the lot of self.

        Examples
        --------
        >>> trade = Trade(..., lot=1.2) / 2
        >>> trade.lot
        0.6
        """
        return self.__mul__(1.0 / num)
