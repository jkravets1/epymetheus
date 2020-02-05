import pytest  # noqa

import random
import numpy as np
import pandas as pd

from epymetheus import Universe, Trade, TradeStrategy
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader

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


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_dataframe(seed, n_bars, n_assets, n_trades):
    universe = make_randomwalk(n_bars=n_bars, n_assets=n_assets, seed=seed)
    strategy = RandomTrader(n_trades=n_trades, seed=seed).run(universe)

    frame_history = pd.DataFrame(strategy.history)
    frame_transaction = pd.DataFrame(strategy.transaction)
    frame_wealth = pd.DataFrame(strategy.wealth)
