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
    >>> # TODO
    """

    def __init__(self, prices, name=None):
        self.prices = prices
        self.name = name

        self.__check_prices()
        self.__init_hash()

    def __check_prices(self):
        if np.isnan(self.prices).any(None):
            raise ValueError("Price has NA.")
        if np.isinf(self.prices).any(None):
            raise ValueError("Price has INF.")
        if not self.bars.is_unique:
            raise ValueError("Bars are not unique.")
        if not self.assets.is_unique:
            raise ValueError("Assets are not unique.")

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
        self._hash_bar = dict(zip(self.bars, list(range(self.bars.size))))
        self._hash_asset = dict(zip(self.assets, list(range(self.assets.size))))
        self._bar_to_index = np.vectorize(lambda bar: self._hash_bar.get(bar, -1))
        self._asset_to_index = np.vectorize(
            lambda asset: self._hash_asset.get(asset, -1)
        )

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
        >>> import pandas as pd
        >>> universe = Universe(pd.DataFrame({
        ...     "AAPL": [1, 1, 1],
        ...     "MSFT": [1, 1, 1],
        ...     "AMZN": [1, 1, 1],
        ... }, index=["2000-01-01", "2000-01-02", "2000-01-03"]))
        >>> universe.bars
        Index(['2000-01-01', '2000-01-02', '2000-01-03'], dtype='object')
        >>> universe.get_bar_indexer('2000-01-02')
        array([1])
        >>> universe.get_bar_indexer(['2000-01-02', '2000-01-01'])
        array([1, 0])
        """
        return self._bar_to_index(bar).reshape(-1)

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
        >>> import pandas as pd
        >>> universe = Universe(pd.DataFrame({
        ...     "AAPL": [1, 1, 1],
        ...     "MSFT": [1, 1, 1],
        ...     "AMZN": [1, 1, 1],
        ... }))
        >>> universe.assets
        Index(['AAPL', 'MSFT', 'AMZN'], dtype='object')
        >>> universe.get_asset_indexer('MSFT')
        array([1])
        >>> universe.get_asset_indexer(['MSFT', 'AAPL'])
        array([1, 0])
        """
        return self._asset_to_index(asset).reshape(-1)
