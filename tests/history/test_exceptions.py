import pytest

from epymetheus import TradeStrategy, History
from epymetheus.exceptions import NotRunError


class SampleStragegy(TradeStrategy):
    """
    A sample strategy.
    """

    def __init__(self):
        pass

    def logic(self, universe):
        pass


# --------------------------------------------------------------------------------


def test_notrunerror():
    strategy = SampleStragegy()

    with pytest.raises(NotRunError):
        History(strategy)
