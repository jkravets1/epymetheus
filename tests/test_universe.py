import pytest
from ._utils import make_randomuniverse, generate_trades

import random
import pandas as pd
import numpy as np

from epymetheus import Trade, TradeStrategy, Universe


list_seed = [42]
list_n_bars = [10, 1000]
list_n_assets = [1, 100]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', list_seed)
@pytest.mark.parametrize('n_bars', list_n_bars)
@pytest.mark.parametrize('n_assets', list_n_assets)
def test_assets(seed, n_bars, n_assets):
    np.random.seed(seed); random.seed(seed)

    universe = make_randomuniverse(n_bars, n_assets)

    assert universe.n_bars == n_bars
    assert universe.n_assets == n_assets

    new_bars = [f'newbar{i}' for i in range(n_bars)]
    new_assets = [f'newasset{i}' for i in range(n_assets)]

    universe.bars = new_bars
    universe.assets = new_assets

    assert list(universe.bars) == new_bars
    assert list(universe.assets) == new_assets




