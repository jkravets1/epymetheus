import random

import numpy as np

from epymetheus import Trade, TradeStrategy


class DeterminedTrader(TradeStrategy):
    """
    Yield given trades.

    Parameters
    ----------
    trade : iterable of Trade
        Trades to yield.
    """
    def __init__(self, trades):
        self.trades = trades

    def logic(self, universe):
        for trade in self.trades:
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
    def __init__(
        self,
        n_trades=100,
        max_n_orders=5,
        max_lot=100,
        min_lot=-100,
        seed=None,
    ):
        self.__n_trades = n_trades
        self.max_n_orders = max_n_orders
        self.max_lot = max_lot
        self.min_lot = min_lot
        self.seed = seed

    def logic(self, universe):
        if self.seed is not None:
            np.random.seed(self.seed)
            random.seed(self.seed)

        for _ in range(self.__n_trades):
            n_orders = np.random.randint(1, self.max_n_orders + 1, size=1)[0]

            asset = random.sample(list(universe.assets), n_orders)
            lot = (self.max_lot - self.min_lot) \
                * np.random.rand(n_orders) - self.min_lot
            open_bar, shut_bar = sorted(random.sample(list(universe.bars), 2))

            yield Trade(
                asset=asset, lot=lot, open_bar=open_bar, shut_bar=shut_bar
            )
