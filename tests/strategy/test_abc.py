import pytest

from epymetheus import TradeStrategy


class StrategyWithoutLogic(TradeStrategy):
    """
    Strategy without logic.
    """

    def __init__(self, param=None):
        self.param = param


# --------------------------------------------------------------------------------


class TestABC:
    def test_abc_abstract(self):
        """
        One cannot instantiate `TradeStrategy` itself.
        """
        with pytest.raises(TypeError):
            TradeStrategy()

    def test_abc_nologic(self):
        """
        One cannot instantiate strategy without logic.
        """
        with pytest.raises(TypeError):
            StrategyWithoutLogic()
