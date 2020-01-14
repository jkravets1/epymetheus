import pandas as pd

try:
    from pandas_datareader.data import DataReader
except ImportError as e:
    print(e)

from ..universe import Universe


tickers = [
    'AAPL',
    'MSFT',
    'AMZN',
    'BRK-A',
    'JPM',
    'JNJ',
    'WMT',
    'BAC',
    'PG',
    'XOM',
]

date_range = pd.date_range('2000-01-01', '2019-12-31')


def fetch_one(ticker, begin, end):
    return DataReader(
        ticker, 'yahoo', begin, end,
    )['Adj Close'].rename(ticker)


def fetch_usstock(tickers=tickers, date_range=date_range):
    b = date_range[0] - pd.tseries.offsets.Day(10)
    e = date_range[-1]

    prices = pd.concat([
        fetch_one(ticker, b, e) for ticker in tickers
    ], axis=1)

    prices = prices.reindex(pd.date_range(b, e)).ffill()
    prices = prices.reindex(date_range)

    return Universe(prices, name='US Stocks')
