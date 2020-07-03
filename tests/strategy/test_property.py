import pytest  # noqa: F401

from epymetheus import TradeStrategy


class SampleStrategy(TradeStrategy):
    """
    This is my favorite strategy.

    Everybody loves this strategy.
    """

    def __init__(self, param0=None, param1=None):
        self.param0 = param0
        self.param1 = param1

    def logic(self, univers):
        pass


# --------------------------------------------------------------------------------


class TestProperty:
    def test_name(self):
        sample_strategy = SampleStrategy()
        assert sample_strategy.name == "SampleStrategy"

    def test_description(self):
        sample_strategy = SampleStrategy()
        assert (
            sample_strategy.description
            == "This is my favorite strategy.\n\nEverybody loves this strategy."
        )

    def test_params(self):
        sample_strategy = SampleStrategy(param0=0.0, param1=1.0)
        assert sample_strategy.params == {"param0": 0.0, "param1": 1.0}
