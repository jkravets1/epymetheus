import pytest

from epymetheus import TradeStrategy
from epymetheus.exceptions import NoTradeError
from epymetheus.datasets import make_randomwalk


class NoTradeStrategy(TradeStrategy):
    """
    Yields no strategy.
    """

    def logic(self, universe):
        pass


params_verbose = [True, False]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize("verbose", params_verbose)
def test_notradeerror(verbose):
    strategy = NoTradeStrategy()
    universe = make_randomwalk()

    with pytest.raises(NoTradeError):
        strategy.run(universe, verbose=verbose)
