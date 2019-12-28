import pandas as pd


class Asset():
    """
    Represent an asset.

    Attributes
    ----------
    - ticker : str
        Ticker of the asset.
    - path : str
        Local path to save the historical data.
    - name : str, default ``ticker``
        Full name of the asset.
    """
    def __init__(
        self,
        ticker: str,
        path: str,
        name=None,
    ):
        """
        Initializes self.
        """
        self.ticker = ticker
        self.path = path
        self.name = name or ticker
        self._price = None

    def __str__(self):
        return self.ticker

    @property
    def price(self):
        """
        Return historical price.

        Returns
        -------
        pandas.DataFrame
            Single column dataframe of daily historical data.
        """
        if self._price is not None:
            return self._price

        try:
            df = pd.read_csv(
                self.path, index_col=0, parse_dates=True, names=[self.ticker]
            )
        except FileNotFoundError as e:
            raise e
        else:
            self._price = df
            return df

    @property
    def begin_date(self):
        """First date when data is available."""
        return self.price.index[0]

    @property
    def end_date(self):
        """Last date when data is available."""
        return self.price.index[-1]

    def to_fig(
        self,
        path: str,
        begin_date=None,
        end_date=None,
        normalize=None,
    ):
        """
        Plot self.

        Parameters
        ----------
        - path: str, path object or file-like object
            Path of the graph.
        - begin_date: datetime.date, default None
            Begin date to plot the data. If None, the very beginning.
        - end_date: datetime.date, optional
            The end date to plot the data. If None, the very end.
        - normalize: float, default None
            If specified, normalize the data so that
            the value at the begin date is this value.
        """
        df = self.read(begin_date=begin_date, end_date=end_date)
        if normalize is not None:
            df /= df.iloc[0] / normalize
        df.to_fig(path, title=self.name)
