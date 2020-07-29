import pytest

import pandas as pd

from epymetheus import Universe, Trade
from epymetheus.benchmarks import BuyAndHold


class TestBuyAndHold:
    def test(self):
        universe = Universe(
            pd.DataFrame({"A": [1, 2, 3], "B": [2, 3, 4], "C": [3, 4, 5]})
        )
        strategy = BuyAndHold({"A": 0.5, "B": 0.5}).run(universe)

        assert len(strategy.trades) == 1
        assert (strategy.trades[0].asset == ["A", "B"]).all()
        assert (strategy.trades[0].lot == [0.5 / 1, 0.5 / 2]).all()
        assert strategy.trades[0].open_bar == 0
        assert strategy.trades[0].close_bar == 2
