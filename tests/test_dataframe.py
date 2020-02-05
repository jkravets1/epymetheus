import pytest  # noqa

import random
import numpy as np
import pandas as pd

from epymetheus import Universe, Trade, TradeStrategy

params_seed = [42, 1, 2, 3]
params_n_bars = [100, 1000]
params_n_assets = [10, 100]  # >= 5
params_n_trades = [10, 100]


def make_universe(n_bars, n_assets, pricedata=None):
    if pricedata is None:
        pricedata = 100 + np.random.randn(n_bars, n_assets).cumsum(axis=0)
    prices = pd.DataFrame(
        pricedata,
        index=[pd.Timestamp('2000-01-01') + pd.Timedelta(days=i) for i in range(n_bars)],
        columns=[f'Asset{i}' for i in range(n_assets)],
    )
    return Universe(prices)


class RandomStrategy(TradeStrategy):
    """
    Yield trades randomly.
    """
    def logic(self, universe, n_trades):
        for trade in generate_trades(universe, n_trades):
            yield trade


def generate_trades(universe, n_trades):
    """
    Yield trades randomly.
    """
    for _ in range(n_trades):
        n_orders = np.random.randint(1, 5)
        asset = random.sample(list(universe.assets), n_orders)
        lot = 20 * np.random.rand(n_orders) - 10  # -10 ~ +10
        open_bar, close_bar = sorted(random.sample(list(universe.bars), 2))
        yield Trade(
            asset=asset, lot=lot, open_bar=open_bar, close_bar=close_bar
        )


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_dataframe(seed, n_bars, n_assets, n_trades):
    universe = make_universe(n_bars, n_assets)
    strategy = RandomStrategy(n_trades=n_trades).run(universe)

    frame_history = pd.DataFrame(strategy.history)
    frame_transaction = pd.DataFrame(strategy.transaction)
    frame_wealth = pd.DataFrame(strategy.wealth)
