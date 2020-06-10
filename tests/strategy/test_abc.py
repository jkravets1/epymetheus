import pytest

from epymetheus import TradeStrategy


class StrategyWithoutLogic(TradeStrategy):
    """
    Strategy without logic.
    """

    def __init__(self, param=None):
        self.param = None


# --------------------------------------------------------------------------------


def test_abc_abstract():
    """
    One cannot instantiate `TradeStrategy` itself.
    """
    with pytest.raises(TypeError):
        strategy = TradeStrategy()  # noqa: F841


def test_abc_nologic():
    """
    One cannot instantiate strategy without logic.
    """
    with pytest.raises(TypeError):
        strategy = StrategyWithoutLogic()  # noqa: F841
