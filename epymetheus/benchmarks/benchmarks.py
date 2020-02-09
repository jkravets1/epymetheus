import random

import numpy as np

from epymetheus import Trade, TradeStrategy


class SingleTradeStrategy(TradeStrategy):
    """
    Yield a single trade.

    Parameters
    ----------
    trade : Trade
        Trade to yield.
    """
    def logic(self, universe, trade):
        yield trade


class RandomTrader(TradeStrategy):
    """
    Yield trades randomly.

    Parameters
    ----------
    - n_trades : int, default 100
        Number of trades to yield.
    - max_n_orders : int, default 5
        Maximum number of orders in a single trade.
    - max_lot : 100
        Maximum value of lots.
    - min_lot : -100
        Minimum value of lots.
    - seed : int, default None
        Seed of randomness. If None, seed is not set.
    """
    def logic(
        self,
        universe,
        n_trades=100,
        max_n_orders=5,
        max_lot=100,
        min_lot=-100,
        seed=None,
    ):
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        for _ in range(n_trades):
            n_orders = np.random.randint(1, max_n_orders + 1, size=1)[0]
            print(n_orders)

            asset = random.sample(list(universe.assets), n_orders)
            lot = (max_lot - min_lot) * np.random.rand(n_orders) - min_lot
            open_bar, shut_bar = sorted(random.sample(list(universe.bars), 2))

            yield Trade(
                asset=asset,
                lot=lot,
                open_bar=open_bar,
                shut_bar=shut_bar,
            )
