import random

import numpy as np
import pandas as pd

from epymetheus import Trade, Universe


def make_randomuniverse(n_bars, n_assets):
    prices = pd.DataFrame(
        100 + np.random.randn(n_bars, n_assets).cumsum(axis=0),
    )
    assets = [f'Asset{i}' for i in range(n_assets)]
    # bars = [pd.Timestamp('2000-01-01') + pd.Timedelta(days=i) for i in range(n_bars)]
    return Universe(prices, assets=assets)


def generate_trades(universe, lots, n_trades):
    """
    Randomly generate params of trades `n_trades` times.

    Yields
    ------
    trade : Trade
    """
    for _ in range(n_trades):
        asset = random.choice(universe.assets)
        lot = random.choice(lots)
        open_bar, shut_bar = sorted(random.sample(list(universe.bars), 2))
        yield Trade(
            asset=asset, lot=lot, open_bar=open_bar, shut_bar=shut_bar
        )
