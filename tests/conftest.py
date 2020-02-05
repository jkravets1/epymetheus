import pytest

import random

import numpy as np
import pandas as pd

from epymetheus import Trade, Universe



def _make_randomuniverse(n_bars, n_assets):
    prices = pd.DataFrame(
        100 + np.random.randn(n_bars, n_assets).cumsum(axis=0),
    )
    assets = [f'Asset{i}' for i in range(n_assets)]
    # bars = [pd.Timestamp('2000-01-01') + pd.Timedelta(days=i) for i in range(n_bars)]
    return Universe(prices, assets=assets)


def _generate_trades(universe, n_trades, max_n_orders=5):
    """
    Yield trades randomly.
    """
    for _ in range(n_trades):
        n_orders = np.random.randint(1, max_n_orders + 1)

        asset = random.sample(list(universe.assets), n_orders)
        lot = 20 * np.random.rand(n_orders) - 10  # -10 ~ +10
        open_bar, shut_bar = sorted(random.sample(list(universe.bars), 2))

        yield Trade(
            asset=asset, lot=lot, open_bar=open_bar, shut_bar=shut_bar,
        )


@pytest.fixture
def make_randomuniverse():
    return _make_randomuniverse


@pytest.fixture
def generate_trades():
    return _generate_trades
