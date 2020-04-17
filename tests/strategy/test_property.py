import pytest

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


def test_name():
    sample_strategy = SampleStrategy()
    assert sample_strategy.name == 'SampleStrategy'


def test_description():
    sample_strategy = SampleStrategy()
    assert sample_strategy.description == \
        "This is my favorite strategy.\n\nEverybody loves this strategy."


def test_params():
    sample_strategy = SampleStrategy(param0=0.0, param1=1.0)
    assert sample_strategy.params == {'param0': 0.0, 'param1': 1.0}
