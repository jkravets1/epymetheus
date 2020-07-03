import pytest

import numpy as np
import pandas as pd

from epymetheus import Universe, Trade
from epymetheus.exceptions import NotRunError
from epymetheus.benchmarks import RandomTrader, DeterminedTrader
from epymetheus.datasets import make_randomwalk
from epymetheus.metrics import Return
from epymetheus.metrics import FinalWealth
from epymetheus.metrics import Drawdown
from epymetheus.metrics import MaxDrawdown
from epymetheus.metrics import Volatility
from epymetheus.metrics import SharpeRatio
from epymetheus.metrics import TradewiseSharpeRatio
from epymetheus.metrics import Exposure
from epymetheus.metrics import _metric_from_name

# TODO fix seed
# TODO
# SharpeRatio
# TradewiseSharpeRatio
# Exposure

class TestBase:
    params_metric = [
        Return,
        FinalWealth,
        Drawdown,
        MaxDrawdown,
        Volatility,
        SharpeRatio,
        TradewiseSharpeRatio,
        Exposure,
    ]

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_result(self, MetricClass):
        m = MetricClass()
        strategy = RandomTrader(seed=42).run(make_randomwalk(seed=42))
        result0 = np.array(m.result(strategy))  # from metric method
        result1 = np.array(strategy.evaluate(m))  # from strategy method
        assert np.equal(result0, result1).all()

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_call(self, MetricClass):
        """
        `metric.result` and `metric.__call__` give the same result
        """
        m = MetricClass()
        strategy = RandomTrader(seed=42).run(make_randomwalk(seed=42))
        result0 = np.array(m.result(strategy))  # from `result` method
        result1 = np.array(m(strategy))  # from __call__
        assert np.equal(result0, result1).all()

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_metric_from_name(self, MetricClass):
        m = MetricClass()
        assert _metric_from_name(m.name).__class__ == m.__class__

    def test_metric_from_name_nonexistent(self):
        """
        `_metric_from_name` is supposed to raise ValueError
        when one gives it a nonexistent metric name.
        """
        with pytest.raises(ValueError):
            _metric_from_name("nonexistent_metric")

    @pytest.mark.parametrize("MetricClass", params_metric)
    def test_notrunerror(self, MetricClass):
        """
        Metric is supposed to raise NotRunError when one tries to evaluate it
        for a strategy which has not been run yet.
        """
        m = MetricClass()
        with pytest.raises(NotRunError):
            RandomTrader(seed=42).evaluate(m)


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
        strategy = RandomTrader(seed=42).run(make_randomwalk(seed=42), budget=budget)
        series_wealth = budget + strategy.wealth.wealth
        result = m.result(strategy)
        result_from_wealth = m._result_from_wealth(series_wealth)
        assert np.allclose(result, result_from_wealth)


class TestFinalWealth:
    MetricClass = FinalWealth

    def test_result_zero(self):
        series_wealth = np.zeros(100, dtype=float)

        result = self.MetricClass()._result_from_wealth(series_wealth)
        expected = 0.0

        assert result == expected

    @pytest.mark.parametrize("seed", range(1))
    def test_result_random(self, seed):
        np.random.seed(seed)
        series_wealth = np.random.rand(100)
        result = self.MetricClass()._result_from_wealth(series_wealth)
        expected = series_wealth[-1]
        assert result == expected

    def test_result(self, seed):
        m = self.MetricClass()
        strategy = RandomTrader(seed=42).run(make_randomwalk(seed=42))

        result0 = m.result(strategy)
        result1 = m._result_from_wealth(strategy.wealth.wealth)

        assert result0 == result1


class TestDrawdown:
    MetricClass = Drawdown

    @pytest.mark.parametrize("rate", [True, False])
    def test_result_zero(self, rate):
        series_wealth = np.ones(100, dtype=float)

        result = self.MetricClass(rate=rate)._result_from_wealth(series_wealth)
        expected = np.zeros(100, dtype=float)

        assert np.allclose(result, expected)

    @pytest.mark.parametrize("rate", [True, False])
    def test_result_hand(self, rate):
        series_wealth = np.array([3, 1, 4, 1, 5, 9, 2], dtype=float)
        result = self.MetricClass(rate=rate)._result_from_wealth(series_wealth)
        if rate:
            expected = np.array([0, -2 / 3, 0, -3 / 4, 0, 0, -7 / 9], dtype=float)
        else:
            expected = np.array([0, -2, 0, -3, 0, 0, -7], dtype=float)
        assert np.allclose(result, expected)

    @pytest.mark.parametrize("seed", range(1))
    @pytest.mark.parametrize("rate", [True, False])
    def test_result(self, seed, rate):
        m = self.MetricClass(rate=rate)
        strategy = RandomTrader(seed=seed).run(make_randomwalk(seed=seed))

        result0 = m.result(strategy)
        result1 = m._result_from_wealth(strategy.wealth.wealth)

        assert np.equal(result0, result1).all()


class TestMaxDrawdown:
    MetricClass = MaxDrawdown

    @pytest.mark.parametrize("rate", [True, False])
    def test_result_zero(self, rate):
        series_wealth = np.ones(100, dtype=float)

        result = self.MetricClass(rate=rate)._result_from_wealth(series_wealth)
        expected = 0

        assert result == expected

    @pytest.mark.parametrize("rate", [True, False])
    def test_result_hand(self, rate):
        series_wealth = np.array([3, 1, 4, 1, 5, 9, 2], dtype=float)
        result = self.MetricClass(rate=rate)._result_from_wealth(series_wealth)
        if rate:
            expected = -7 / 9
        else:
            expected = -7
        assert np.allclose(result, expected)

    @pytest.mark.parametrize("seed", range(1))
    @pytest.mark.parametrize("rate", [True, False])
    def test_result(self, seed, rate):
        m = self.MetricClass(rate=rate)
        strategy = RandomTrader(seed=seed).run(make_randomwalk(seed=seed))

        result0 = m.result(strategy)
        result1 = m._result_from_wealth(strategy.wealth.wealth)

        assert np.allclose(result0, result1)


class TestVolatility:
    MetricClass = Volatility

    @pytest.mark.parametrize("rate", [True, False])
    def test_result_zero(self, rate):
        series_wealth = np.arange(1.0, 2.0, 0.01, dtype=float)
        print(series_wealth)

        if rate:
            series_wealth = np.exp(series_wealth)

        result = self.MetricClass(rate=rate)._result_from_wealth(series_wealth)
        expected = 0

        assert np.allclose(result, expected)

    @pytest.mark.parametrize("rate", [False])
    def test_result_hand(self, rate):
        series_wealth = np.array([3, 1, 4], dtype=float)

        result = self.MetricClass(rate=rate)._result_from_wealth(series_wealth)
        if rate:
            expected = np.std([-2 / 3, 3 / 1])
        else:
            expected = np.std([-2, 3])
        assert np.allclose(result, expected)
