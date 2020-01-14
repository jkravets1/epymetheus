import pandas as pd
from pandas_datareader.data import DataReader
from pandas.tseries.offsets import DateOffset
import matplotlib.pyplot as plt
import seaborn

from pandas.plotting import register_matplotlib_converters

from epymetheus import Universe, Trade, TradeStrategy

register_matplotlib_converters()
seaborn.set_style('ticks')

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
]  # N/A: GOOG, FB, V, MA
date_range = pd.date_range('2000-01-01', '2019-12-31')


def fetch_equity(ticker, begin, end):
    return DataReader(
        ticker, 'yahoo', begin, end,
    )['Adj Close'].rename(ticker)


def fetch_equities(tickers, date_range):
    # return pd.read_csv('US Equity.csv', index_col=0, parse_dates=True)
    b = date_range[0] - pd.tseries.offsets.Day(10)
    e = date_range[-1]

    prices = pd.concat([
        fetch_equity(ticker, b, e) for ticker in tickers
    ], axis=1)

    prices = prices.reindex(pd.date_range(b, e)).ffill()
    prices = prices.reindex(date_range)

    return prices


class SimpleTrendFollower(TradeStrategy):
    """
    A simple trend-following strategy.
    Buys stocks for a month with the highest percentile of one month returns.

    Parameters
    ----------
    - percentile : float
        The threshold to buy or sell.
        E.g. If 0.1, buy stocks with returns of highest 10%.
    """
    def logic(self, universe, percentile, bet):

        watch_period = DateOffset(months=1)
        trade_period = DateOffset(months=1)
        n_trade = int(universe.n_assets * percentile)

        def trade_open_dates(universe, watch_period, trade_period):
            """Yield begin_date of trades."""
            open_date = universe.bars[0] + watch_period
            while open_date + trade_period <= universe.bars[-1]:
                yield open_date
                open_date += trade_period

        def tot_returns(open_date):
            """Return 1 month return of assets as Series."""
            b = open_date - DateOffset(days=1)
            e = open_date - DateOffset(months=1)
            return universe.data.loc[e, :] / universe.data.loc[b, :]

        for open_date in trade_open_dates(universe, watch_period, trade_period):
            close_date = open_date + trade_period
            r = tot_returns(open_date)
            assets_sorted = sorted(universe.assets, key=lambda asset: r[asset])

            for asset in assets_sorted[-n_trade:]:
                lot = bet / universe.data.at[open_date, asset]
                yield Trade(asset=asset, lot=lot, open_date=open_date, close_date=close_date)


def plot(strategy):
    plt.figure(figsize=(16, 4))
    df_wealth = pd.DataFrame(strategy.wealth)
    df_wealth.index = strategy.universe.bars
    plt.plot(df_wealth, linewidth=1)
    plt.title('Wealth')
    plt.ylabel('wealth / dollars')
    plt.savefig('wealth.png', bbox_inches="tight", pad_inches=0.1)

    plt.figure(figsize=(8, 8))
    plt.hist(strategy.history.gains, bins=100)
    plt.axvline(0, ls='--', color='red')
    plt.title('Gains')
    plt.savefig('gains.png', bbox_inches="tight", pad_inches=0.1)

    plt.figure(figsize=(16, 4))
    exposure_lot = pd.DataFrame(strategy.transaction).cumsum(axis=0).values
    exposure_price = exposure_lot * strategy.universe.data.values
    exposure = exposure_price.sum(axis=1)
    df_exposure = pd.Series(exposure, index=strategy.universe.bars)
    plt.figure(figsize=(8, 8))
    plt.plot(df_exposure)
    plt.axhline(0, ls='--', color='gray')
    plt.title('Exposure')
    plt.savefig('exposure.png', bbox_inches="tight", pad_inches=0.1)


def main():
    prices = fetch_equities(tickers, date_range)
    universe = Universe(prices, name='US Equity')

    strategy = SimpleTrendFollower(percentile=0.2, bet=10000)
    strategy.run(universe, verbose=True)

    plot(strategy)


if __name__ == '__main__':
    main()

