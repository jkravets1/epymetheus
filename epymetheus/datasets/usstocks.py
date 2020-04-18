from os.path import dirname
from pathlib import Path

import pandas as pd
from pandas_datareader import DataReader

from epymetheus import Universe
from ._utils import ffill_and_cut

module_path = Path(dirname(__file__))


def fetch_usstocks(
    begin_date='2000-01-01',
    end_date='2019-12-31',
    n_assets=10,
    column='Adj Close',
    verbose=True,
):
    """
    Return Universe of US stocks.

    Parameters
    ----------
    - begin_date : str
    - end_date : str
    - n_assets : int

    Returns
    -------
    universe : Universe
    """
    begin_date = pd.Timestamp(begin_date)
    end_date = pd.Timestamp(end_date)

    with open(module_path / 'usstocks.txt') as f:
        tickers = [ticker.strip() for ticker in f.readlines()]

    if n_assets > len(tickers):
        raise ValueError('n_assets should be <=', len(tickers))

    prices = pd.DataFrame({
        ticker: ffill_and_cut(
            DataReader(
                name=ticker,
                data_source='yahoo',
                start=begin_date - pd.Timedelta(days=10),
                end=end_date,
            )[column],
            begin_date=begin_date,
        )
        for ticker in tickers[:n_assets]
    })

    return Universe(prices)
