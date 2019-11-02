from typing import List

import pandas as pd
import pathlib

from epymetheus.core.asset import Asset


class Universe(pd.core.frame.DataFrame):
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
    def __init__(
        self,
        data=None,
        index=None,
        columns=None,
        name=None,
        unit=None,
        **kwargs,
    ):
        """Initialize self."""
        super(Universe, self).__init__(
            data=data,
            index=index,
            columns=columns,
            **kwargs,
        )
        self.name = name
        self.unit = unit

    @property
    def begin_date(self):
        """Return begin date of period."""
        return self.index[0]

    @property
    def end_date(self):
        """Return end date of period."""
        return self.index[-1]

    @property
    def duration(self):
        """Return duration of period."""
        return self.end_date - self.begin_date

    @classmethod
    def read_assets(
        cls,
        assets: List[Asset],
        name=None,
        unit=None,
        begin_date=None,
        end_date=None
    ):
        """
        Initialize self from a list of Assets by reading local data.

        Parameters
        ----------
        - assets : list of Asset
            List of assets to read local data.
        - name : str, optional
            Name of the universe.
        - begin_date : datetime.date, default None
            Begin date of the universe. If None, the very beginning.
        - end_date : datetime.date, default None
            End date of the universe. If None, the very end.

        Returns
        -------
        Universe
        """
        df = pd.concat([a.price for a in assets], axis=1)
        df = df.loc[begin_date or df.begin_date: end_date or df.end_date, :]
        return cls(data=df, name=name, unit=unit)

    @classmethod
    def read_directory(
        cls,
        directory: str,
        name=None,
        begin_date=None,
        end_date=None,
        unit=None,
        **kwargs,
    ):
        """
        Initialize self by reading all data in a directory.

        Parameters
        ----------
        - directory : str, path object or file-like object
            The directory where the data is read.
        - name : str, default None
            Name of the universe. If none, the name of ``directory``.
        - begin_date : datetime.date
            Begin date to read data. If None, the very beginning.
        - end_date : datetime.date
            End date to read data. If None, the very end.

        Return
        ------
        Universe
        """
        try:
            list_f = pathlib.Path(directory).glob('*.csv')
            name = name or pathlib.Path(directory).stem
        except FileNotFoundError as e:
            raise e

        df = pd.concat([pd.read_csv(f, index_col=0, parse_dates=True, **kwargs)
                        for f in list_f], axis=1)
        df = df.loc[begin_date or df.index[0]: end_date or df.index[-1], :]
        return cls(data=df, name=name, unit=unit)
