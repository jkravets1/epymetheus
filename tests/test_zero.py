import pytest
from ._utils import make_randomuniverse

import pandas as pd
import numpy as np

from epymetheus import TradeStrategy, Universe
from epymetheus.datasets import make_randomwalk


list_seed = [42]
list_n_bars = [10, 1000]
list_n_assets = [1, 100]


class VoidStrategy(TradeStrategy):
    """Yield no trade."""
    def logic(self, universe):
        pass


@pytest.mark.parametrize('seed', list_seed)
@pytest.mark.parametrize('n_bars', list_n_bars)
@pytest.mark.parametrize('n_assets', list_n_assets)
def test_void(seed, n_bars, n_assets):
    universe = make_randomuniverse(n_bars, n_assets)

    strategy = VoidStrategy().run(universe)

    assert strategy.history.assets.size == 0
    assert strategy.history.lots.size == 0
    assert strategy.history.open_bars.size == 0
    assert strategy.history.close_bars.size == 0
    # assert strategy.history.durations.size == 0
    assert strategy.history.open_prices.size == 0
    assert strategy.history.close_prices.size == 0
    assert strategy.history.gains.size == 0

    # TODO test transaction, wealth
