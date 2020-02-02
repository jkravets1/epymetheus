import pytest
from ._utils import make_randomuniverse

import random
import numpy as np


params_seed = [42]
params_n_bars = [10, 1000]
params_n_assets = [1, 100]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_assets(seed, n_bars, n_assets):
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomuniverse(n_bars, n_assets)

    assert universe.n_bars == n_bars
    assert universe.n_assets == n_assets

    new_bars = [f'newbar{i}' for i in range(n_bars)]
    new_assets = [f'newasset{i}' for i in range(n_assets)]

    universe.bars = new_bars
    universe.assets = new_assets

    assert list(universe.bars) == new_bars
    assert list(universe.assets) == new_assets
