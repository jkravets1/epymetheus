import pytest  # noqa

import random
import numpy as np
import pandas as pd

from epymetheus import Universe, Trade, TradeStrategy
# from epymetheus.pipe import (
#     atakes,
#     acuts,
#     _signal_closebar,
#     _signal_lastbar,
#     _acumpnl,
#     _close_by_signals,
# )

params_seed = [42]
params_n_bars = [100, 1000]
params_n_assets = [10, 100]
params_n_trades = [10, 100]


def make_universe(n_bars, n_assets, pricedata=None):
    if pricedata is None:
        pricedata = np.zeros((n_bars, n_assets))
    prices = pd.DataFrame(
        pricedata,
        index=[f'Bar{i}' for i in range(n_bars)],
        columns=[f'Asset{i}' for i in range(n_assets)],
    )
    return Universe(prices)


class MockStrategy(TradeStrategy):
    def logic(self, universe):
        pass


def make_strategy(universe=None, trades=None):
    """
    Return strategy with attributes universe and trades.

    Returns
    -------
    strategy : TradeStrategy
    """
    strategy = MockStrategy()
    if universe:
        strategy.universe = universe
    if trades:
        strategy.trades = trades
    return strategy


# --------------------------------------------------------------------------------


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_bars', params_n_bars)
# @pytest.mark.parametrize('n_assets', params_n_assets)
# @pytest.mark.parametrize('n_trades', params_n_trades)
# def test_lastbar(seed, n_bars, n_assets, n_trades):
#     universe = make_universe(n_bars, n_assets)
#     strategy = make_strategy(universe=universe)

#     lastbar = _signal_lastbar(strategy)

#     assert lastbar[:-1].all()
