import pytest
from ._utils import make_randomuniverse

from epymetheus import TradeStrategy


class StrategyWithoutLogic(TradeStrategy):
    """strategy without logic."""
    pass


class SampleStrategy(TradeStrategy):
    """
    This is my favorite strategy.
    """
    def logic(universe, param0=0.0, param1=1.0):
        pass


# --------------------------------------------------------------------------------


def test_abc():
    with pytest.raises(TypeError):
        # Can't instantiate abstract class TradeStrategy with abstract methods logic
        strategy = TradeStrategy()

    with pytest.raises(TypeError):
        # Can't instantiate abstract class TradeStrategy with abstract methods logic
        strategy = StrategyWithoutLogic()


def test_name():
    strategy = SampleStrategy()

    assert strategy.name == 'SampleStrategy'
    assert strategy.description == 'This is my favorite strategy.'
