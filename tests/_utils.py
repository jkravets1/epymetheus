import random

import numpy as np
import pandas as pd

from epymetheus import Universe


def make_randomuniverse(n_bars, n_assets):
    assets = np.arange(n_assets).astype(str)
    prices = pd.DataFrame(
        100 + np.random.randn(n_bars, n_assets).cumsum(axis=0),
        columns=assets,
    )
    return Universe(prices)


def generate_trades(universe, lots, n_trades):
    """
    Randomly generate params of trades `n_trades` times.

    Yields
    ------
    - (asset, lot, open_bar, close_bar)
        * asset is in universe.asset
        * lot is in lots
        * open_bar, close_bar are in universe.bars and open_bar < close_bar
    """
    for _ in range(n_trades):
        asset = random.choice(universe.assets)
        lot = random.choice(lots)
        open_bar, close_bar = sorted(random.sample(list(universe.bars), 2))
        yield (asset, lot, open_bar, close_bar)
