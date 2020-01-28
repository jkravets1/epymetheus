from pathlib import Path

import pandas as pd

from .utils.check import check_prices


class Universe:
    """
    Store historical prices of multiple assets.

    Parameters
    ----------
    - name : str
        Name of universe.
    - data : `pandas.DataFrame`
        Historical prices.

    Attributes
    ----------
    - bars : array-like, shape (n_bars, )
        Bars.  Alias of `self.data.index`.
    - assets : array-like, shape (n_assets, )
        Assets.  Alias of `self.data.columns`.

    Examples
    --------
    Initializing:
    >>> data
    array([[ 1234.5  3456.7  ... ]
           [ 1235.6  3457.8  ... ]
             ......  ......  ...
           [ 1236.7  3458.9  ... ]])
    >>> bars
    array(['2000-01-01', '2000-01-02', ..., '2019-12-31'])
    >>> assets
    array(['AAPL', 'MSFT', ...])
    >>> universe = Universe(
    ...     data=data,
    ...     bars=bars,
    ...     assets=assets,
    ...     name='US Equity',
    ... )

    Show as `pandas.DataFrame`:
    >>> universe.to_frame()
                  AAPL    MSFT  ...
    2000-01-01  1234.5  3456.7  ...
    2000-01-02  1235.6  3457.8  ...
    ..........  ......  ......  ...
    2018-12-31  1236.7  3458.9  ...

    Read csv files:
    >>> csvs
    ['data/AAPL.csv', 'data/MSFT.csv', ...]
    >>> universe = Universe.read_csvs(
    ...     name='US Equity', csvs=csvs,
    ...     index_col=0, parse_dates=True,
    ... )
    """
    def __init__(self, prices, name=None):
        """Initialize self."""
        # TODO accept data other than pandas.DataFrame
        check_prices(prices)
        self.prices = prices
        self.name = name

    @property
    def bars(self):
        return self.prices.index

    @bars.setter
    def bars(self, value):
        self.prices.index = value

    @property
    def n_bars(self):
        return len(self.bars)

    @property
    def assets(self):
        return self.prices.columns

    @assets.setter
    def assets(self, value):
        self.prices.columns = value

    @property
    def n_assets(self):
        return len(self.assets)

    @classmethod
    def read_csv(cls, csv, name=None, begin_bar=None, end_bar=None, **kwargs):
        name = name or Path(csv).stem
        prices = pd.read_csv(csv, **kwargs)

        prices = prices.loc[begin_bar or prices.index[0]:
                            end_bar or prices.index[-1]]

        return cls(prices, name=name)

    def read_csvs(cls,
                  csvs,
                  name=None,
                  begin_bar=None,
                  end_bar=None,
                  assets=None,
                  **kwargs):
        prices = pd.concat([
            pd.read_csv(csv, **kwargs) for csv in csvs
        ], axis=1)
        prices = prices.loc[begin_bar or prices.index[0]:
                            end_bar or prices.index[-1]]
        if assets is not None:
            prices.columns = assets

        return cls(prices, name=name)
