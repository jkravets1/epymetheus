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


# @pytest.fixture(scope="function", autouse=True)
# def set_seed():
#     np.random.seed(42)


class TestExecute:
    pass


class TestArrayValue:
    universe_hand = Universe(
        pd.DataFrame(
            {"A0": [3, 1, 4, 1, 5, 9, 2], "A1": [2, 7, 1, 8, 2, 8, 1],},
            index=range(7),
            dtype=float,
        )
    )
    trade0 = Trade(asset=["A0", "A1"], lot=[2, -3], open_bar=1, shut_bar=3)
    trade1 = Trade(asset=["A1", "A0"], lot=[-3, 2], open_bar=1, shut_bar=3)
    expected0 = [[6, -6], [2, -21], [8, -3], [2, -24], [10, -6], [18, -24], [4, -3]]
    expected1 = [[-6, 6], [-21, 2], [-3, 8], [-24, 2], [-6, 10], [-24, 18], [-3, 4]]

    @pytest.mark.parametrize(
        "trade, expected", [(trade0, expected0), (trade1, expected1)],
    )
    def test_value_hand(self, trade, expected):
        result = trade._array_value(universe=self.universe_hand)
        assert np.allclose(result, expected)


class TestArrayExposure:
    universe_hand = Universe(
        pd.DataFrame(
            {"A0": [3, 1, 4, 1, 5, 9, 2], "A1": [2, 7, 1, 8, 2, 8, 1],},
            index=range(7),
            dtype=float,
        )
    )

    trade0 = Trade(asset=["A0", "A1"], lot=[2, -3], open_bar=1, shut_bar=3)
    trade1 = Trade(asset=["A1", "A0"], lot=[-3, 2], open_bar=1, shut_bar=3)
    expected0 = [[0, 0], [2, -21], [8, -3], [2, -24], [0, 0], [0, 0], [0, 0]]
    expected1 = [[0, 0], [-21, 2], [-3, 8], [-24, 2], [0, 0], [0, 0], [0, 0]]

    @pytest.mark.parametrize(
        "trade, expected", [(trade0, expected0), (trade1, expected1)],
    )
    def test_hand(self, trade, expected):
        result = trade.array_exposure(universe=self.universe_hand)
        assert np.allclose(result, expected)


class TestSeriesExposure:
    # TODO before and after execution
    universe_hand = Universe(
        pd.DataFrame(
            {"A0": [3, 1, 4, 1, 5, 9, 2], "A1": [2, 7, 1, 8, 2, 8, 1],},
            index=range(7),
            dtype=float,
        )
    )

    @pytest.mark.parametrize("net", [True, False])
    def test_hand(self, net):
        trade = Trade(asset=["A0", "A1"], lot=[2, -3], open_bar=1, shut_bar=3)
        result = trade.series_exposure(net=net, universe=self.universe_hand)
        if net:
            expected = [0, -19, 5, -22, 0, 0, 0]
        else:
            expected = [0, 23, 11, 26, 0, 0, 0]

        assert np.allclose(result, expected)


class TestSeriesPnl:
    universe_hand = Universe(
        pd.DataFrame(
            {"A0": [3, 1, 4, 1, 5, 9, 2], "A1": [2, 7, 1, 8, 2, 8, 1],},
            index=range(7),
            dtype=float,
        )
    )
    trade0 = Trade(asset=["A0", "A1"], lot=[2, -3], open_bar=1, shut_bar=3)
    expected0 = [0, 0, 24, -3, -3, -3, -3]

    @pytest.mark.parametrize("trade, expected", [(trade0, expected0)])
    def test_value_hand(self, trade, expected):
        result = trade.series_pnl(universe=self.universe_hand)
        assert np.allclose(result, expected)

    pass


class TestFinalPnl:
    pass


# @pytest.mark.parametrize("seed", params_seed)
# def test_execute_0_0(seed):
#     """
#     Test `trade.execute` sets `trade.close_bar` correctly.

#     Setup
#     -----
#     - trade.take is None
#     - trade.stop is None
#     - trade.shut_bar is not None

#     Expected Result
#     ---------------
#     trade.close_bar == universe.shut_bar
#     """
#     # shut_bar is not None
#     universe = make_randomwalk(seed=seed)
#     trade = make_random_trade(universe, seed=seed)
#     trade.execute(universe)

#     assert trade.close_bar == trade.shut_bar


# @pytest.mark.parametrize("seed", params_seed)
# def test_execute_0_1(seed):
#     """
#     Test `trade.execute` sets `trade.close_bar` correctly.

#     Setup
#     -----
#     - trade.take is None
#     - trade.stop is None
#     - trade.shut_bar is None

#     Expected Result
#     ---------------
#     trade.close_bar == universe.bars[-1]
#     """
#     # shut_bar is not None
#     universe = make_randomwalk(seed=seed)
#     trade = make_random_trade(universe, seed=seed)
#     trade.shut_bar = None
#     trade.execute(universe)

#     assert trade.close_bar == universe.bars[-1]


# @pytest.mark.parametrize("seed", params_seed)
# def test_execute(seed):
#     """
#     Test `trade.execute` sets `trade.close_bar` correctly.

#     Setup
#     -----
#     - trade.take is None
#     - trade.stop is None
#     - trade.shut_bar is None

#     Expected Result
#     ---------------
#     trade.close_bar == universe.bars[-1]
#     """
#     # shut_bar is not None
#     universe = make_randomwalk(seed=seed)
#     trade = make_random_trade(universe, seed=seed)
#     trade.shut_bar = None
#     trade.execute(universe)

#     assert trade.close_bar == universe.bars[-1]


# # @pytest.mark.parametrize('seed', params_seed)
# # @pytest.mark.parametrize('n_bars', params_n_bars)
# # @pytest.mark.parametrize('const', params_const)
# # def test_execute(seed, n_bars, const):
# #     period = n_samples // 10
# #     shift = np.random.randint(period)
# #     prices = pd.DataFrame({
# #         'Asset0': const + make_sin(n_bars=n_bars, period=period, shift=shift)
# #     })
# #     universe = Universe(prices)

# #     trade = Trade('Asset0', lot=1.0, )


# # def test_execute_take():
# #     universe = Universe(prices=pd.DataFrame({"Asset0": np.arange(100, 200)}))

# #     trade = Trade("Asset0", lot=1.0, take=1.9, open_bar=1, shut_bar=5)
# #     trade.execute(universe)
# #     assert trade.close_bar == 3
# #     assert np.array_equal(trade.final_pnl(universe), [103 - 101])

# #     trade = Trade("Asset0", lot=2.0, take=3.8, open_bar=1, shut_bar=5)
# #     trade.execute(universe)
# #     assert trade.close_bar == 3
# #     assert np.array_equal(trade.final_pnl(universe), [2 * (103 - 101)])

# #     trade = Trade("Asset0", lot=1.0, take=1000, open_bar=1, shut_bar=5)
# #     trade.execute(universe)
# #     assert trade.close_bar == 5
# #     assert np.array_equal(trade.final_pnl(universe), [105 - 101])


# # def test_execute_stop():
# #     universe = Universe(prices=pd.DataFrame({"Asset0": np.arange(100, 0, -1)}))

# #     trade = Trade("Asset0", lot=1.0, stop=-1.9, open_bar=1, shut_bar=5)
# #     trade.execute(universe)
# #     assert trade.close_bar == 3
# #     assert np.array_equal(trade.final_pnl(universe), [97 - 99])

# #     trade = Trade("Asset0", lot=2.0, stop=-3.8, open_bar=1, shut_bar=5)
# #     trade.execute(universe)
# #     assert trade.close_bar == 3
# #     assert np.array_equal(trade.final_pnl(universe), [2 * (97 - 99)])

# #     trade = Trade("Asset0", lot=1.0, stop=-1000, open_bar=1, shut_bar=5)
# #     trade.execute(universe)
# #     assert trade.close_bar == 5
# #     assert np.array_equal(trade.final_pnl(universe), [95 - 99])


class TestRepr:
    """
    Test `Trade.__repr__`.
    """

    def test_value(self):
        asset = "A0"
        open_bar = "B0"
        shut_bar = "B1"
        lot = 1.0
        take = 2.0
        stop = -2.0
        trade = Trade(
            asset=asset,
            open_bar=open_bar,
            shut_bar=shut_bar,
            lot=lot,
            take=take,
            stop=stop,
        )
        expected = "Trade(asset='A0', open_bar='B0', shut_bar='B1', lot=1.0, take=2.0, stop=-2.0)"
        assert repr(trade) == expected

    def test_repr(self):
        asset = "A0"
        trade = Trade(asset=asset)
        expected = "Trade(asset='A0', lot=1.0)"  # default value of lot = 1.0
        assert repr(trade) == expected


# # TODO both take and stop
# # TODO short position
# # TODO multiple orders

# # def test_execute_takestop():
# #     pass
