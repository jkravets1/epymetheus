import pytest  # noqa

import pandas as pd

from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader


params_seed = [42, 1, 2, 3]
params_n_bars = [100, 1000]
params_n_assets = [10, 100]
params_n_trades = [10, 100]


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
    print(frame_history)
    print(frame_transaction)
    print(frame_wealth)
