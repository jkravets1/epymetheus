import pytest  # noqa: F401

import pandas as pd

from epymetheus import Strategy, Universe, Trade


class SampleStrategy(Strategy):
    """
    This is my favorite strategy.

    Everybody loves this strategy.
    """

    def __init__(self, param0=None, param1=None):
        self.param0 = param0
        self.param1 = param1

    def logic(self, univers):
        yield Trade(asset=["A0", "A1"])
        yield Trade(asset=["A2", "A3"])


# --------------------------------------------------------------------------------


class TestProperty:

    universe = Universe(pd.DataFrame({f"A{i}": range(10) for i in range(4)}))

    def test_name(self):
        strategy = SampleStrategy()
        assert strategy.name == "SampleStrategy"

    def test_description(self):
        strategy = SampleStrategy()
        assert (
            strategy.description
            == "This is my favorite strategy.\n\nEverybody loves this strategy."
        )

    def test_params(self):
        strategy = SampleStrategy(param0=0.0, param1=1.0)
        assert strategy.params == {"param0": 0.0, "param1": 1.0}

    def test_is_run(self):
        strategy = SampleStrategy()
        assert strategy.is_run == False
        strategy.run(self.universe)
        assert strategy.is_run == True

    def test_n_trades(self):
        strategy = SampleStrategy().run(self.universe)
        assert strategy.n_trades == 2

    def test_n_orders(self):
        strategy = SampleStrategy().run(self.universe)
        assert strategy.n_orders == 4
