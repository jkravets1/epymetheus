import pytest

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from epymetheus import Trade, History, Universe
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import DeterminedTrader, RandomTrader


class TestBase:
    def _get_history(self):
        universe = make_randomwalk(seed=42)
        strategy = RandomTrader(seed=42).run(universe)
        return History(strategy)

    def test_strategy_attr(self):
        """
        `History.__init__` and `strategy.history` are supposed to give the same results.
        """
        universe = make_randomwalk(seed=42)
        strategy = RandomTrader(seed=42).run(universe)

        result0 = pd.DataFrame(History(strategy))  # from History.__init__
        result1 = pd.DataFrame(strategy.history)  # from strategy.history

        assert_frame_equal(result0, result1)

    def test_trade_keys(self):
        """
        Test if history has the expected columns.
        """
        history = self._get_history()
        assert set(history.keys()) == {
            "order_id",
            "trade_id",
            "asset",
            "lot",
            "open_bar",
            "close_bar",
            "shut_bar",
            "take",
            "stop",
            "pnl",
        }


class TestColumn:

    universe = Universe(
        pd.DataFrame(
            {f"A{i}": range(10) for i in range(10)}, index=[f"B{i}" for i in range(10)]
        )
    )

    trades = [
        Trade(
            asset=["A0", "A1"],
            lot=[1, 2],
            open_bar="B0",
            shut_bar="B8",
            take=1.0,
            stop=-1.0,
        ),
        Trade(
            asset=["A2", "A3"],
            lot=[3, 4],
            open_bar="B1",
            shut_bar="B9",
            take=2.0,
            stop=-2.0,
        ),
    ]

    def _get_history(self):
        strategy = DeterminedTrader(trades=self.trades).run(self.universe)
        return History(strategy)

    def test_trade_id(self):
        result = self._get_history().trade_id
        assert np.array_equal(result, [0, 0, 1, 1])

    def test_order_id(self):
        result = self._get_history().order_id
        assert np.array_equal(result, [0, 1, 2, 3])

    def test_asset(self):
        result = self._get_history().asset
        assert np.array_equal(result, ["A0", "A1", "A2", "A3"])

    def test_open_bar(self):
        result = self._get_history().open_bar
        assert np.array_equal(result, ["B0", "B0", "B1", "B1"])

    def test_shut_bar(self):
        result = self._get_history().shut_bar
        assert np.array_equal(result, ["B8", "B8", "B9", "B9"])

    def test_take(self):
        result = self._get_history().take
        assert np.array_equal(result, [1.0, 1.0, 2.0, 2.0])

    def test_stop(self):
        result = self._get_history().stop
        assert np.array_equal(result, [-1.0, -1.0, -2.0, -2.0])

    def test_pnl(self):
        pass  # TODO
