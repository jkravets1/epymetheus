from os.path import dirname
from pathlib import Path
import yaml

import pandas as pd
from pandas_datareader.data import DataReader

from ..universe import Universe


module_path = Path(dirname(__file__))


def fetch_usstocks(
    begin_date='2000-01-01',
    end_date='2019-01-01',
    n_assets=10,
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
    fetcher = _USStockFetcher(
        begin_date=begin_date, end_date=end_date, n_assets=n_assets
    )
    prices = fetcher.fetch(verbose=verbose)
    return Universe(prices, name='USStocks')


class _USStockFetcher:
    """
    Fetch US Stocks from yahoo finance.
    """
    with open(module_path / 'usstocks.yml') as f:
        tickers = yaml.load(f, Loader=yaml.FullLoader)

    def __init__(self, begin_date, end_date, n_assets):
        self.begin_date = pd.Timestamp(begin_date)
        self.end_date = pd.Timestamp(end_date)
        self.n_assets = n_assets

        # make beginning date early enough for the case
        # that begin_date is a holiday
        self.begin_date_before = self.begin_date - pd.Timedelta(days=30)

    def fetch_one(self, ticker):
        """
        Return a single historical price fetched from yahoo finance.

        Returns
        -------
        pandas.Series
        """
        price = DataReader(ticker, 'yahoo', self.begin_date, self.end_date)
        price = price['Adj Close'].rename(ticker)
        price = price.reindex(
            pd.date_range(self.begin_date_before, self.end_date)
        )
        price = price.ffill()
        price = price.reindex(
            pd.date_range(self.begin_date, self.end_date)
        )
        if price.isnull().any():
            raise ValueError('Full data not available')
        return price

    def fetch(self, verbose=True):
        tickers = iter(self.tickers)
        data = []
        while len(data) < self.n_assets:
            try:
                ticker = next(tickers)
            except StopIteration:
                raise ValueError(
                    f'Only {len(data)} stocks are available '
                    f'for {self.begin_date}-{self.end_date}'
                )
            try:
                if verbose:
                    print(
                        f'\rFetching {ticker} '
                        f'({len(data) + 1}/{self.n_assets}) ...'
                    )
                price = self.fetch_one(ticker)
            except ValueError:
                pass
            else:
                data.append(price)

        dataframe = pd.concat(data, axis=1)
        if verbose:
            print('Done.')
        return dataframe


if __name__ == '__main__':
    print(fetch_usstocks().prices)
