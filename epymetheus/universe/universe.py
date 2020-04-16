from operator import getitem
from functools import partial
import numpy as np


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
    def __init__(self, prices, name=None):
        self.prices = prices
        self.name = name

        self.__check_prices()
        self.__init_hash()

    def __check_prices(self):
        if np.isnan(self.prices).any(None):
            raise ValueError('Price has NA.')
        if np.isinf(self.prices).any(None):
            raise ValueError('Price has INF.')
        if not self.bars.is_unique:
            raise ValueError('Bars are not unique.')
        if not self.assets.is_unique:
            raise ValueError('Assets are not unique.')

    def __init_hash(self):
        """
        Initialize hash table of assets and bars.

        Following attributes are initialized:

        - self.__hash_bar : dict
            Dict from bar to index.
        - self.__hash_asset : dict
            Dict from asset to index.
        - self.__bar_to_index : callable
            Callable from bar to index.
        - self.__asset_to_index : callable
            Callable from asset to index.
        """
        self._hash_bar = dict(self.bars, list(range(self.bars.size)))
        self._hash_asset = dict(self.assets, list(range(self.assets.size)))
        self._bar_to_index = np.vectorize(partial(getitem, self._hash_bar))
        self._asset_to_index = np.vectorize(partial(getitem, self._hash_asset))

    @property
    def bars(self):
        return self.prices.index

    @property
    def assets(self):
        return self.prices.columns

    @property
    def n_bars(self):
        return self.bars.size

    @property
    def n_assets(self):
        return self.assets.size

    # def _asset_onehot(self, asset_id):
    #     """
    #     Return one-hot vectors of assers from asset names.

    #     Parameters
    #     ----------
    #     - assets : array-like, shape (n, )

    #     Returns
    #     -------
    #     asset_onehot : array, shape (n, n_assets)

    #     Examples
    #     --------
    #     >>> universe.assets
    #     Index(['AAPL', 'MSFT', 'AMZN'], dtype='object')
    #     >>> universe._asset_onehot(['MSFT', 'AAPL'])
    #     array([[0., 1., 0.]
    #            [1., 0., 0.]])
    #     """
    #     return np.eye(self.n_assets)[asset_id]

    def get_bar_indexer(self, bar):
        """
        Return bar indices from names of bars.
        Basically the same with `self.bars.get_indexer`, but much faster.

        Parameters
        ----------
        - bar : array-like, shape (n, )
            Names of bars.

        Returns
        -------
        bar_index : array, shape (n, )

        Examples
        --------
        >>> universe.bars
        Index(['2000-01-01', '2000-01-02', '2000-01-03'], dtype='object')
        >>> universe.get_bar_indexer('2000-01-02')
        array(1)
        >>> universe.get_bar_indexer(['2000-01-02', '2000-01-01'])
        array([1, 0])
        """
        return self._bar_to_index(bar)

    def get_asset_indexer(self, asset):
        """
        Return indices from names of assets.
        Basically the same with `self.assets.get_indexer`, but much faster.

        Parameters
        ----------
        - asset: array-like, shape (n, )
            Names of bars.

        Returns
        -------
        asset_index : array, shape (n, )

        Examples
        --------
        >>> universe.assets
        Index(['AAPL', 'MSFT', 'AMZN'], dtype='object')
        >>> universe.get_asset_indexer('MSFT')
        array(1)
        >>> universe.get_asset_indexer(['MSFT', 'AAPL'])
        array([1, 0])
        """
        return self._asset_to_index(asset)

    # def _bar_onehot(self, bar_ids):
    #     """
    #     Return one-hot vectors from bar names.

    #     Parameters
    #     ----------
    #     - bar_ids : array-like, shape (n, )

    #     Returns
    #     -------
    #     onehot_bars : array, shape (n, n_bars)

    #     Examples
    #     --------
    #     >>> universe.bars
    #     Index(['2000-01-01', '2000-01-02', '2000-01-03'], dtype='object')
    #     >>> universe._bar_onehot(['2000-01-02', '2000-01-01'])
    #     array([[0., 1., 0.]
    #            [1., 0., 0.]])
    #     """
    #     return np.eye(self.n_bars)[bar_ids]

    # def _pick_prices(self, bar_ids, asset_id):
    #     """
    #     Return prices from bar names and asset names.

    #     Parameters
    #     ----------
    #     - bar_ids : array-like, shape (n, )
    #     - asset_ds : array-like, shape (n, )

    #     Returns
    #     -------
    #     prices : array, shape (n, )

    #     Examples
    #     --------
    #     >>> universe.prices
    #            AAPL  MSFT  AMZN
    #     01-01     1    10   100
    #     01-02     2    20   200
    #     01-03     3    30   300
    #     01-04     4    40   400
    #     >>> universe._pick_prices(['AAPL', 'MSFT'], ['01-02', '01-03'])
    #     array([ 2, 30])
    #     """
    #     return self.prices.values[bar_ids, asset_id]
