import pytest

import numpy as np
import pandas as pd

from epymetheus import Universe, Trade
from epymetheus.exceptions import NotRunError
from epymetheus.benchmarks import RandomTrader, DeterminedTrader
from epymetheus.datasets import make_randomwalk
from epymetheus.metrics import Return
from epymetheus.metrics import FinalWealth
from epymetheus.metrics import TradewiseSharpeRatio
from epymetheus.metrics import _metric_from_name

params_metric = [FinalWealth]


class TestBase:

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_result(self, MetricClass):
        m = MetricClass()
        universe = make_randomwalk()
        strategy = RandomTrader().run(universe)
        assert m.result(strategy) == strategy.evaluate(m)

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_notrunerror(self, MetricClass):
        m = MetricClass()
        strategy = RandomTrader()

        with pytest.raises(NotRunError):
            strategy.evaluate(m)

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_init_from_name(self, MetricClass):
        m = MetricClass()
        assert _metric_from_name(m.name).__class__ == m.__class__


class TestReturn:
    """
    Test if `Return` works as expected.
    """

    def test_result_zero(self):
        series_wealth = np.zeros(100)

        result = Return(rate=False)._result_from_wealth(series_wealth)
        expected = np.zeros(100)

        assert np.equal(result, expected).all()

    @pytest.mark.parametrize("rate", [True, False])
    def test_result_hand(self, rate):
        series_wealth = np.array([3, 1, 4, 1, 5, 9, 2], dtype=float)
        result = Return(rate=rate)._result_from_wealth(series_wealth)
        if rate:
            expected = np.array([0, -2 / 3, 3 / 1, -3 / 4, 4 / 1, 4 / 5, -7 / 9])
        else:
            expected = np.array([0, -2, 3, -3, 4, 4, -7], dtype=float)
        assert np.equal(result, expected).all()

    def test_result(self):
        universe = make_randomwalk()
        strategy = RandomTrader().run(universe)
        series_wealth = strategy.wealth.wealth
        result = self.metric.result(strategy)
        result_from_wealth = self.metric._result_from_wealth(series_wealth)
        assert np.equal(result, result_from_wealth).all()

    @pytest.mark.parametrize("rate", [True, False])
    def test_result(self, rate):
        universe = Universe(prices=pd.DataFrame({"Asset0": np.arange(100, 200)}))
        trade = Trade(asset="Asset0", lot=1.0, open_bar=1, shut_bar=5)
        strategy = DeterminedTrader([trade]).run(universe, budget=1.0)

        expected = np.zeros(universe.n_bars)
        expected[trade.open_bar + 1 : trade.shut_bar + 1] = 1.0
        if rate:
            expected /= np.cumsum(expected)
            expected = np.nan_to_num(expected)

        metric = Return(rate=rate)
        result = metric.result(strategy)
        assert np.allclose(result, expected)


class TestFinalWealth:
    def test_result(self):
        metric = FinalWealth()
        universe = make_randomwalk()
        strategy = RandomTrader().run(universe)
        result = metric.result(strategy)
        expected = strategy.wealth.wealth[-1]

        assert result == expected


class TestTradewiseSharpeRatio:
    def test_result(self):
        metric = TradewiseSharpeRatio()
        universe = make_randomwalk()
        strategy = RandomTrader().run(universe)
        result = metric.result(strategy)

        # TODO assert
