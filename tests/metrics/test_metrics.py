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
        strategy = RandomTrader().run(make_randomwalk())
        assert m.result(strategy) == strategy.evaluate(m)

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_notrunerror(self, MetricClass):
        m = MetricClass()
        strategy = RandomTrader()

        with pytest.raises(NotRunError):
            strategy.evaluate(m)

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_call(self, MetricClass):
        m = MetricClass()
        strategy = RandomTrader().run(make_randomwalk())
        assert m.result(strategy) == m(strategy)

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_metric_from_name(self, MetricClass):
        m = MetricClass()
        assert _metric_from_name(m.name).__class__ == m.__class__

    def test_metric_from_name_nonexistent(self):
        with pytest.raises(ValueError):
            _metric_from_name("nonexistent_metric")

class TestReturn:
    """
    Test if `Return` works as expected.
    """
    MetricClass = Return

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

    @pytest.mark.parametrize("rate", [True, False])
    def test_result_from_wealth(self, rate):
        m = self.MetricClass(rate=rate)
        budget = 100
        strategy = RandomTrader().run(make_randomwalk(), budget=budget)
        series_wealth = budget + strategy.wealth.wealth
        result = m.result(strategy)
        result_from_wealth = m._result_from_wealth(series_wealth)
        assert np.allclose(result, result_from_wealth)


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
