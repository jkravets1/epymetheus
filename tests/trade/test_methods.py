import pytest

import numpy as np
import pandas as pd

from epymetheus import Trade, Universe
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader


params_seed = [42, 1, 2, 3]
params_n_bars = [10, 100, 1000]
params_const = [-10, 0, 10]


def make_random_trade(universe, seed):
    random_trader = RandomTrader(n_trades=1, seed=seed).run(universe)
    return random_trader.trades[0]


# def make_sin(n_bars, period, shift):
#     """
#     Make sin curve.

#     Parameters
#     ----------
#     - n_bars : int
#     - period : int
#     - shift : int
#     """
#     return np.sin(2 * np.pi * (np.arange(n_bars) + shift) / period)


# --------------------------------------------------------------------------------


@pytest.fixture(scope='function', autouse=True)
def set_seed():
    np.random.seed(42)


@pytest.mark.parametrize('seed', params_seed)
def test_series_value(seed):
    """
    Test `trade.series_value` returns the correct value.
    """
    universe = make_randomwalk(seed=seed)
    trade = make_random_trade(universe, seed=seed)

    value_expected = np.add.reduce([
        lot * universe.prices[asset]
        for lot, asset in zip(trade.lot, trade.asset)
    ])

    assert np.allclose(trade.series_value(universe), value_expected)


@pytest.mark.parametrize('seed', params_seed)
def test_execute_0_0(seed):
    """
    Test `trade.execute` sets `trade.close_bar` correctly.

    Setup
    -----
    - trade.take is None
    - trade.stop is None
    - trade.shut_bar is not None

    Expected Result
    ---------------
    trade.close_bar == universe.shut_bar
    """
    # shut_bar is not None
    universe = make_randomwalk(seed=seed)
    trade = make_random_trade(universe, seed=seed)
    trade.execute(universe)

    assert trade.close_bar == trade.shut_bar


@pytest.mark.parametrize('seed', params_seed)
def test_execute_0_1(seed):
    """
    Test `trade.execute` sets `trade.close_bar` correctly.

    Setup
    -----
    - trade.take is None
    - trade.stop is None
    - trade.shut_bar is None

    Expected Result
    ---------------
    trade.close_bar == universe.bars[-1]
    """
    # shut_bar is not None
    universe = make_randomwalk(seed=seed)
    trade = make_random_trade(universe, seed=seed)
    trade.shut_bar = None
    trade.execute(universe)

    assert trade.close_bar == universe.bars[-1]


@pytest.mark.parametrize('seed', params_seed)
def test_execute_0_1(seed):
    """
    Test `trade.execute` sets `trade.close_bar` correctly.

    Setup
    -----
    - trade.take is None
    - trade.stop is None
    - trade.shut_bar is None

    Expected Result
    ---------------
    trade.close_bar == universe.bars[-1]
    """
    # shut_bar is not None
    universe = make_randomwalk(seed=seed)
    trade = make_random_trade(universe, seed=seed)
    trade.shut_bar = None
    trade.execute(universe)

    assert trade.close_bar == universe.bars[-1]


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_bars', params_n_bars)
# @pytest.mark.parametrize('const', params_const)
# def test_execute(seed, n_bars, const):
#     period = n_samples // 10
#     shift = np.random.randint(period)
#     prices = pd.DataFrame({
#         'Asset0': const + make_sin(n_bars=n_bars, period=period, shift=shift)
#     })
#     universe = Universe(prices)

#     trade = Trade('Asset0', lot=1.0, )


def test_execute_take():
    universe = Universe(
        prices=pd.DataFrame({
            'Asset0': np.arange(100, 200)
        })
    )

    trade = Trade('Asset0', lot=1.0, take=1.9, open_bar=1, shut_bar=5)
    trade.execute(universe)
    assert trade.close_bar == 3
    assert np.array_equal(trade.pnl, [103 - 101])

    trade = Trade('Asset0', lot=2.0, take=3.8, open_bar=1, shut_bar=5)
    trade.execute(universe)
    assert trade.close_bar == 3
    assert np.array_equal(trade.pnl, [2 * (103 - 101)])

    trade = Trade('Asset0', lot=1.0, take=1000, open_bar=1, shut_bar=5)
    trade.execute(universe)
    assert trade.close_bar == 5
    assert np.array_equal(trade.pnl, [105 - 101])


def test_execute_stop():
    universe = Universe(
        prices=pd.DataFrame({
            'Asset0': np.arange(100, 0, -1)
        })
    )

    trade = Trade('Asset0', lot=1.0, stop=-1.9, open_bar=1, shut_bar=5)
    trade.execute(universe)
    assert trade.close_bar == 3
    assert np.array_equal(trade.pnl, [97 - 99])

    trade = Trade('Asset0', lot=2.0, stop=-3.8, open_bar=1, shut_bar=5)
    trade.execute(universe)
    assert trade.close_bar == 3
    assert np.array_equal(trade.pnl, [2 * (97 - 99)])

    trade = Trade('Asset0', lot=1.0, stop=-1000, open_bar=1, shut_bar=5)
    trade.execute(universe)
    assert trade.close_bar == 5
    assert np.array_equal(trade.pnl, [95 - 99])


# TODO both take and stop
# TODO short position
# TODO multiple orders

# def test_execute_takestop():
#     pass
