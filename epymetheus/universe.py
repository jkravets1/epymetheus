import numpy as np

try:
    from functools import cached_property
except ImportError:
    cached_property = property


class Universe:
    """
    Store historical prices of multiple assets.

    Parameters
    ----------
    - prices : `pandas.DataFrame`
        Historical prices.
    - name : str
        Name of universe.

    Attributes
    ----------
    - bars : pandas.Index, shape (n_bars, )
        Bars.  Alias of `self.data.index`.
    - assets : pandas.Index, shape (n_assets, )
        Assets.  Alias of `self.data.columns`.
    - n_bars : int
        Equal to `len(self.bars)`.
    - n_assets : int
        Equal to `len(self.assets)`.

    Examples
    --------
    >>> ...
    """
    def __init__(self, prices, name=None, bars=None, assets=None):
        self.__check_prices(prices)

        self.prices = prices
        self.name = name
        if bars:
            self.bars = bars
        if assets:
            self.assets = assets

        self.assets = np.array(self.assets).astype(str)

    @property
    def bars(self):
        return self.prices.index

    @bars.setter
    def bars(self, value):
        self.prices.index = value

    @property
    def n_bars(self):
        return self.bars.size

    @property
    def assets(self):
        return self.prices.columns

    @assets.setter
    def assets(self, value):
        self.prices.columns = np.array(value).astype(str)

    @property
    def n_assets(self):
        return self.assets.size

    # @classmethod
    # def read_csv(
    #     cls,
    #     csv,
    #     name=None,
    #     begin_bar=None,
    #     end_bar=None,
    #     bars=None,
    #     assets=None,
    #     **kwargs
    # ):
    #     name = name or Path(csv).stem
    #     prices = pd.read_csv(csv, **kwargs)
    #     prices = prices.loc[
    #         begin_bar or prices.index[0]: end_bar or prices.index[-1]
    #     ]
    #     return cls(prices, name=name, bars=bars, assets=assets)

    # def read_csvs(
    #     cls,
    #     csvs,
    #     name=None,
    #     begin_bar=None,
    #     end_bar=None,
    #     bars=None,
    #     assets=None,
    #     **kwargs
    # ):
    #     prices = pd.concat([
    #         pd.read_csv(csv, **kwargs) for csv in csvs
    #     ], axis=1)
    #     prices = prices.loc[
    #         begin_bar or prices.index[0]: end_bar or prices.index[-1]
    #     ]
    #     return cls(prices, name=name, bars=bars, assets=assets)

    # ------------------------------------------------------------

    def __check_prices(self, prices):
        if np.isnan(prices).any(None):
            raise ValueError('Price has NA.')
        if np.isinf(prices).any(None):
            raise ValueError('Price has INF.')
        if not prices.index.is_unique:
            raise ValueError('Bars are not unique.')
        if not prices.columns.is_unique:
            raise ValueError('Assets are not unique.')

    # def _asset_id(self, assets):
    #     """
    #     Return asset indices from asset names.

    #     Parameters
    #     ----------
    #     - assets : array-like, shape (n, )

    #     Returns
    #     -------
    #     - asset_ids : array, shape (n, )

    #     Examples
    #     --------
    #     >>> universe.assets
    #     Index(['AAPL', 'MSFT', 'AMZN'], dtype='object')
    #     >>> universe._asset_id('MSFT')
    #     array(1)
    #     >>> universe._asset_id(['MSFT', 'AAPL'])
    #     array([1, 0])
    #     """
    #     return self.assets.get_indexer(assets)

    def _asset_onehot(self, asset_ids):
        """
        Return one-hot vectors of assers from asset names.

        Parameters
        ----------
        - assets : array-like, shape (n, )

        Returns
        -------
        asset_onehot : array, shape (n, n_assets)

        Examples
        --------
        >>> universe.assets
        Index(['AAPL', 'MSFT', 'AMZN'], dtype='object')
        >>> universe._asset_onehot(['MSFT', 'AAPL'])
        array([[0., 1., 0.]
               [1., 0., 0.]])
        """
        return np.eye(self.n_assets)[asset_ids]

    def _bar_id(self, bars):
        """
        Return bar indices from bar names.

        Parameters
        ----------
        - bars : array-like, shape (n, )

        Returns
        -------
        bar_ids : array, shape (n, )

        Examples
        --------
        >>> universe.bars
        Index(['2000-01-01', '2000-01-02', '2000-01-03'], dtype='object')
        >>> universe._bar_id('2000-01-02')
        array(1)
        >>> universe._bar_id(['2000-01-02', '2000-01-01'])
        array([1, 0])
        """
        return self.bars.get_indexer(bars)

    def _bar_onehot(self, bar_ids):
        """
        Return one-hot vectors from bar names.

        Parameters
        ----------
        - bar_ids : array-like, shape (n, )

        Returns
        -------
        onehot_bars : array, shape (n, n_bars)

        Examples
        --------
        >>> universe.bars
        Index(['2000-01-01', '2000-01-02', '2000-01-03'], dtype='object')
        >>> universe._bar_onehot(['2000-01-02', '2000-01-01'])
        array([[0., 1., 0.]
               [1., 0., 0.]])
        """
        return np.eye(self.n_bars)[bar_ids]

    def _pick_prices(self, bar_ids, asset_ids):
        """
        Return prices from bar names and asset names.

        Parameters
        ----------
        - bar_ids : array-like, shape (n, )
        - asset_ds : array-like, shape (n, )

        Returns
        -------
        prices : array, shape (n, )

        Examples
        --------
        >>> universe.prices
               AAPL  MSFT  AMZN
        01-01     1    10   100
        01-02     2    20   200
        01-03     3    30   300
        01-04     4    40   400
        >>> universe._pick_prices(['AAPL', 'MSFT'], ['01-02', '01-03'])
        array([ 2, 30])
        """
        return self.prices.values[bar_ids, asset_ids]
