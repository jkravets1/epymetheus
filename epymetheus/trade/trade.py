import numpy as np

from epymetheus.utils.array import catch_first_index


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

    @property
    def array_asset(self):
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
    def array_lot(self):
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
        return self.array_asset.size

    def series_pnl(self, universe, open_bar=None, close_bar=None):
        """
        Return value of the position.

        Returns
        -------
        value : numpy.array, shape (n_bars, )

        Examples
        --------
        >>> universe.prices
              Asset0  Asset1
        Bar0    10.1     0.1
        Bar1    11.1     0.1
        Bar2    12.1     0.1
        Bar3    13.1     0.1
        Bar4    14.1     0.1
        >>> trade.asset
        ['Asset0', 'Asset1']
        >>> trade.lot
        [1.0, -1.0]
        >>> trade.open_bar
        'Bar1'
        >>> trade.close_bar
        'Bar3'
        >>> trade.series_pnl
        array([  0.0  1.0  2.0  2.0  2.0])
        """
        open_bar = open_bar if open_bar is not None else self.open_bar
        close_bar = close_bar if close_bar is not None else self.close_bar

        open_bar_index = universe.get_bar_indexer(open_bar)[0]
        close_bar_index = universe.get_bar_indexer(close_bar)[0]

        series_value = self.series_value(universe)
        series_pnl = series_value - series_value[open_bar_index]
        series_pnl[:open_bar_index] = 0
        series_pnl[close_bar_index:] = series_pnl[close_bar_index]

        return series_pnl

    def array_value(self, universe):
        """
        Return value of the position for each asset.

        Returns
        -------
        value : numpy.array, shape (n_bars, n_orders)

        Examples
        --------
        >>> strategy.universe.prices
              Asset0  Asset1
        Bar0       1      10
        Bar1       2      20
        Bar2       3      30
        Bar3       4      40
        Bar4       5      50
        >>> trade = Trade(asset=['Asset0', 'Asset1'], lot=[-1.0, 1.0], ...)
        >>> trade.array_value
        array([[  -1   10]
               [  -2   20]
               [  -3   30]
               [  -4   40]
               [  -5   50])]
        """
        p = universe.prices.iloc[
            :, universe.get_asset_indexer(self.asset)
        ].values
        # (n_orders, ) * (n_bars, n_orders) -> (n_bars, n_orders)
        return self.lot * p

    def series_value(self, universe):
        """
        Return time-series of value of the position.

        Returns
        -------
        series_value : numpy.array, shape (n_bars, )

        Examples
        --------
        >>> strategy.universe.prices
              Asset0  Asset1
        Bar0       1      10
        Bar1       2      20
        Bar2       3      30
        Bar3       4      40
        Bar4       5      50
        >>> trade = Trade(asset=['Asset0', 'Asset1'], lot=[-1.0, 1.0], ...)
        >>> trade.series_value
        array([   9  18  27  36  45])
        """
        return self.array_value(universe).sum(axis=1)

    def execute(self, universe):
        """
        Execute trade according to `take`, `stop` and `shut_bar`.  It sets:
        - self.close_bar
            Bar at which self is closed.
        - self.pnl
            Profit and loss of self for each order.

        Parameters
        ----------
        universe : Universe

        Returns
        -------
        self : Trade

        Examples
        --------
        >>> universe.prices
              Asset0  Asset1
        Bar0    10.1     0.1
        Bar1    11.1     0.1
        Bar2    12.1     0.1
        Bar3    13.1     0.1
        Bar4    14.1     0.1
        >>> trade = Trade(
        ...     asset=['Asset0', 'Asset1'],
        ...     lot=[1.0, -1.0],
        ...     open_bar='Bar1',
        ...     take=1.9,
        ... )
        >>> trade.execute(universe)
        >>> trade.close_bar
        'Bar3'
        >>> trade.pnl
        array([2.0  0.0])
        """
        array_value = self.array_value(universe)

        open_bar_index = universe.get_bar_indexer(self.open_bar)[0]
        close_bar_index = self.__get_close_bar_index(universe, array_value)

        self.close_bar = universe.bars[close_bar_index]
        self.pnl = (
            array_value[close_bar_index, :]
            - array_value[open_bar_index, :]
        )

        return self

    def __get_close_bar_index(self, universe, array_value):
        """
        Used in self.execute

        Returns
        -------
        close_bar_index : int
        """
        if self.shut_bar is not None:
            timeout_index = universe.get_bar_indexer(self.shut_bar)[0]
        else:
            timeout_index = universe.n_bars - 1

        if self.take is None and self.stop is None:
            return timeout_index
        else:
            open_bar_index = universe.get_bar_indexer(self.open_bar)[0]

            # Don't use self.series_value; save time
            series_value = array_value.sum(axis=1)
            profit = series_value - series_value[open_bar_index]
            profit[:open_bar_index] = 0

            signal_take = profit >= (self.take or np.inf)
            signal_stop = profit <= (self.stop or -np.inf)
            close_bar_index = catch_first_index(
                np.logical_or(signal_take, signal_stop)
            )

            if close_bar_index == -1 or close_bar_index > timeout_index:
                return timeout_index
            else:
                return close_bar_index

    def __mul__(self, num):
        """
        Multiply lot of self.

        Examples
        --------
        >>> trade = -2.0 * Trade(..., lot=1.2)
        >>> trade.lot
        -2.4
        """
        self.lot = num * self.array_lot
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
