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

params_metric = [FinalWealth]


class TestBase:

    @pytest.mark.parametrize("metric", params_metric)
    def test_result(self, metric):
        metric = metric()
        universe = make_randomwalk()
        strategy = RandomTrader().run(universe)
        assert metric.result(strategy) == strategy.evaluate(metric)

    @pytest.mark.parametrize("metric", params_metric)
    def test_notrunerror(self, metric):
        metric = metric()
        strategy = RandomTrader()

        with pytest.raises(NotRunError):
            strategy.evaluate(metric)


class TestReturn:

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
