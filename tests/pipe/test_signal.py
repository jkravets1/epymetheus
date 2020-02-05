import pytest  # noqa

import random
import numpy as np
import pandas as pd

from epymetheus import Universe, Trade, TradeStrategy
from epymetheus.pipe.signal import (
    _signal_shutbar,
    _signal_lastbar,
    _signal_opening,
    _acumpnl,
)

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


def test_signal_shutbar():
    universe = make_universe(4, 3)
    trades = [
        Trade(asset=['Asset0', 'Asset1'], lot=[1, -2], open_bar='Bar0', shut_bar='Bar1'),
        Trade(asset=['Asset2', 'Asset1'], lot=[3, 4], open_bar='Bar1', shut_bar='Bar3'),
    ]
    strategy = make_strategy(universe=universe, trades=trades)

    expected = np.array([
        [False, False],
        [ True, False],
        [False, False],
        [False,  True],
    ])

    assert np.equal(_signal_shutbar(strategy), expected).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_signal_lastbar(seed, n_bars, n_assets, n_trades):
    universe = make_universe(n_bars, n_assets)
    trades = [
        Trade(
            asset=['Asset0', 'Asset1'],
            lot=[1, 1],
            open_bar='Bar0',
            shut_bar='Bar1'
        ),
        Trade(
            asset=['Asset2', 'Asset1'],
            lot=[1, 1],
            open_bar='Bar0',
            shut_bar='Bar2'
        ),
    ]
    strategy = make_strategy(universe=universe, trades=trades)

    lastbar = _signal_lastbar(strategy)

    assert (~lastbar[:-1, :]).all()
    assert lastbar[-1, :].all()


def test_signal_opening():
    universe = make_universe(3, 3)
    trades = [
        Trade(
            asset=['Asset0', 'Asset1'],
            lot=[1, 1],
            open_bar='Bar0',
            shut_bar='Bar1'
        ),
        Trade(
            asset=['Asset2', 'Asset1'],
            lot=[1, 1],
            open_bar='Bar0',
            shut_bar='Bar2'
        ),
    ]
    strategy = make_strategy(universe=universe, trades=trades)

    opening_expected = np.array([
        [False, False],
        [True, True],
        [False, True],
    ])

    assert np.equal(_signal_opening(strategy), opening_expected).all()
