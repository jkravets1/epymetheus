import pandas as pd
from pandas.tseries.offsets import DateOffset
import matplotlib.pyplot as plt
import seaborn
from pandas.plotting import register_matplotlib_converters

from epymetheus import Trade, TradeStrategy
from epymetheus.datasets import fetch_usstocks

register_matplotlib_converters()
seaborn.set_style('ticks')


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

    @staticmethod
    def sorted_assets(universe, open_date):
        """
        Return list of asset sorted according to one-month returns.
        Sort is ascending (poor-return first).

        Returns
        -------
        list
        """
        onemonth_returns = universe.prices.loc[open_date] \
            / universe.prices.loc[open_date - DateOffset(months=1)]
        return list(onemonth_returns.sort_values().index)

    def logic(self, universe, percentile, bet_price, atake, acut):
        n_trade = int(universe.n_assets * percentile)
        date_range = pd.date_range(universe.bars[0], universe.bars[-1], freq='BM')
        hold_period = DateOffset(months=3)

        for open_date in date_range[1:]:
            assets = self.sorted_assets(universe, open_date)
            for asset in assets[:n_trade]:
                lot = bet_price / universe.prices.at[open_date, asset]
                yield Trade(
                    asset=asset, lot=lot,
                    open_bar=open_date,
                    shut_bar=open_date + hold_period,
                    atake=atake, acut=acut,
                )


def plot(strategy):
    plt.figure(figsize=(16, 4))
    df_wealth = pd.DataFrame(strategy.wealth).set_index('bars')
    plt.plot(df_wealth, linewidth=1)
    plt.title('Wealth / USD')
    plt.savefig('wealth.png', bbox_inches="tight", pad_inches=0.1)

    plt.figure(figsize=(16, 4))
    plt.hist(strategy.history.gains, bins=100)
    plt.axvline(0, ls='--', color='red')
    plt.title('Gains')
    plt.savefig('gains.png', bbox_inches="tight", pad_inches=0.1)

    df_exposure = pd.Series(strategy.net_exposure, index=strategy.universe.bars)

    plt.figure(figsize=(16, 4))
    plt.plot(df_exposure)
    plt.axhline(0, ls='--', color='gray')
    plt.title('Net exposure')
    plt.savefig('exposure.png', bbox_inches="tight", pad_inches=0.1)

    pd.DataFrame(strategy.history).to_csv('history.csv')


def main():
    universe = fetch_usstocks(n_assets=10)

    strategy = SimpleTrendFollower(
        percentile=0.2,
        bet_price=10000,
        atake=10000,
        acut=-1000,
    )
    strategy.run(universe)

    plot(strategy)


if __name__ == '__main__':
    main()
