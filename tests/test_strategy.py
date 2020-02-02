import pytest

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
        strategy = TradeStrategy()
        print(strategy)

    with pytest.raises(TypeError):
        strategy = StrategyWithoutLogic()
        print(strategy)


def test_name():
    strategy = SampleStrategy()

    assert strategy.name == 'SampleStrategy'
    assert strategy.description == 'This is my favorite strategy.'
