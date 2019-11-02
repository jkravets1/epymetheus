import datetime
from dateutil.relativedelta import relativedelta

import epymetheus as ep


class SimpleMeanReversion(ep.TradeStrategy):
    """
    A simple trend-following strategy that buys stocks for a month with
    the lowest percentile one month returns and sells the highest percentile returns.

    Parameters
    ----------
    - percentile : float
        The threshold to buy or sell.
        E.g. If 0.1, buy/sell stocks with returns of lowest/highest 10%.
    """

    def logic(self, universe, percentile):

        train_period = relativedelta(months=1)
        trade_period = relativedelta(months=1)

        def trade_bds(universe, train_period, trade_period):
            """Yield begin dates of trade periods."""
            d = universe.begin_date + train_period
            while d + trade_period <= universe.end_date:
                yield d
                d += trade_period

        def tot_return(asset, begin_date, end_date):
            """Return total return of asset from begin_date to end_date."""
            b, e = universe.at[begin_date, asset], universe.at[end_date, asset]
            return e / b - 1

        num_buysell = int(len(universe.columns) * percentile)

        for trade_bd in trade_bds(universe, train_period, trade_period):
            train_bd = trade_bd - train_period
            trade_ed = trade_bd + trade_period - relativedelta(days=1)
            train_ed = train_bd + train_period - relativedelta(days=1)

            key = lambda asset: tot_return(asset, train_bd, train_ed)
            buy = sorted(universe.columns, key=key)[:num_buysell]
            sell = sorted(universe.columns, key=key)[-num_buysell:]

            yield ep.Trade(
                quote={asset: 1 for asset in buy},
                begin_date=trade_bd, end_date=trade_ed,
            )
            yield ep.Trade(
                quote={asset: -1 for asset in sell},
                begin_date=trade_bd, end_date=trade_ed,
            )


def main():
    universe = ep.Universe.read_directory(
        directory='data/hist/JP Equity/',
        begin_date=datetime.date(2000, 1, 1),
        end_date=datetime.date(2018, 12, 31),
    )
    trend_follower = SimpleMeanReversion(percentile=0.1)
    trend_follower.run(universe)


if __name__ == '__main__':
    main()
