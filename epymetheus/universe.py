import pandas as pd

class Universe:
    """
    Dataframe comprising historical data of multiple assets.

    Inheriting ``pandas.DataFrame``.

    Parameters
    ----------
    - name : str
        Name of the universe.
    - data : ndarray, Iterable, dict, DataFrame
        Array of the historical price data.
    - columns : index, array-like
        The list of asset tickers.
    - index : index, array-like of datetime.date
        Period of the historical price data.
    """
    def __init__(self, name, data):
        """Initialize self."""
        self.name = name
        self.data = data

    def __str__(self):
        return (
            f'Universe: {self.name}'
            f' {self.begin_date} - {self.end_date}'
            f' {self.assets}'
        )

    @property
    def assets(self):
        return list(self.data.columns)

    @property
    def begin_date(self):
        """Return begin date of period."""
        return self.data.index[0].date()

    @property
    def end_date(self):
        """Return end date of period."""
        return self.data.index[-1].date()

    @classmethod
    def read_csv(cls, name, csv,
                 begin_date=None, end_date=None,
                 **kwargs):
        """
        Initialize Universe by reading csv.

        Parameters
        ----------
        - name : str
        - csv : path of csv file
        - begin_date : date, default None
            Begin date to read data. If None, the very beginning.
        - end_date : date, default None
            End date to read data. If None, the very end.
        - kwargs
            Other parameters passed to `pandas.read_csv`.
        """
        data = pd.read_csv(csv, kwargs)
        data = data.loc[begin_date or data.index[0]: end_date or data.index[-1]]
        return cls(name=name, data=data)

    @classmethod
    def read_csvs(cls, name, csvs,
                 begin_date=None, end_date=None,
                  **kwargs):
        """
        Initialize self by reading iterable of csvs.

        Parameters
        ----------
        - name : str
        - csvs : Iterable of csv
        - begin_date : date, default None
            Begin date to read data. If None, the very beginning.
        - end_date : date, default None
            End date to read data. If None, the very end.
        """
        data = pd.concat([
            pd.read_csv(f, **kwargs) for f in csvs
        ], axis=1, sort=True)
        data = data.loc[begin_date or data.index[0]: end_date or data.index[-1]]
        return cls(name=name, data=data)
