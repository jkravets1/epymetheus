import pandas as pd

from epymetheus import AllocationStrategy


class FixedWeight(AllocationStrategy):
    """
    Allocate the wealth with a fixed weight.

    Parameters
    ----------
    - weight : dict
        The allocation weight in terms of the price.
    - rebalance : DateOffset object or string, default '1D'
        The period to rebalance the portfolio.
    """
    def logic(universe, weight: dict, rebalance='1D'):
        w = pd.DataFrame(weight, index=universe.index)
        r = (
            (1 + universe.pct_change(fill_method='ffill'))
            .cumprod().fillna(1.0)
        )
        r /= r.asfreq(rebalance).reindex(r.index, method='ffill')
        df = w * r
        df = df.div(df.sum(axis=1), axis=0).mul(w.sum(axis=1), axis=0)
        return df


class EqualWeight(FixedWeight):
    """
    Allocate the wealth with the equal weight in terms of the price.

    Parameters
    ----------
    - rebalance : DateOffset object or string, default '1D'
        The period to rebalance the portfolio.
    """
    def logic(universe, rebalance='1D'):
        weight = {asset: 1 / len(universe.columns)
                  for asset in universe.columns}
        return super.logic(weight=weight, rebalance=rebalance)


class BestStock(FixedWeight):
    """
    Allocate the whole wealth to the best stock in whole period.
    """
    def logic(universe):
        best_stock = (universe.iloc[-1] / universe.iloc[0]).idxmax()
        return super.logic(weight={best_stock: 1})


class MinVariance(AllocationStrategy):
    pass  # TODO
