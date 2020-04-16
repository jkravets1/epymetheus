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

    Attributes
    ----------
    - close_bar : object
        Bar to close the trade.
        It is set by the method `self.execute`.

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
    def n_orders(self):
        return self._array_lot.size

    def value(self, universe):
        """
        Return value of the position.

        Returns
        -------
        value : numpy.array, shape (n_bars, )

        Examples
        --------
        >>> strategy.universe.prices
               Asset0  Asset1
        01-01       1      10
        01-02       2      20
        01-03       3      30
        01-04       4      40
        01-05       5      50
        >>> trade = Trade(asset=['Asset0', 'Asset1'], lot=[-1.0, 1.0], ...)
        >>> trade.value
        array([ 9, 18, 27, 36, 45])
        """
        return np.dot(
            self.array_lot,
            universe.prices.iloc[:, universe.get_asset_indexer(self.asset)]
        )

    def execute(self, universe):
        """
        Execute trade according to `take`, `stop` and `shut_bar`.
        It sets `self.close_bar`.

        Parameters
        ----------
        universe : Universe

        Returns
        -------
        self : Trade
        """
        open_bar_index = universe.get_bar_indexer(self.open_bar)
        shut_bar_index = universe.get_bar_indexer(self.shut_bar)

        position_value = self.value
        pnl = position_value - position_value[open_bar_index]

        # array of shape (n_bars, ); True when trade has opened
        opening = np.array([i >= open_bar_index for i in range(universe.n_bars)])

        # array of shape (n_bars, ); True at shut_bar
        signal_shut = np.array([i >= shut_bar_index for i in range(universe.n_bars)])
        # array of shape (n_bars, ); True when pnl > take
        signal_take = (pnl > (self.take or np.inf))
        # array of shape (n_bars, ); True when pnl < stop
        signal_stop = (pnl < (self.stop or -np.inf))

        signal = opening and (signal_shut or signal_take or signal_stop)

        close_bar_index = catch_first_index(signal)

        if close_bar_index == -1:
            close_bar_index = universe.n_bars - 1

        self.close_bar = universe.bars[close_bar_index]

        return self

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
