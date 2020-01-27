import pytest

import pandas as pd
import numpy as np

from epymetheus import TradeStrategy, Universe
from epymetheus.datasets import make_randomwalk


class VoidStrategy(TradeStrategy):
    """Yield no trade."""
    def logic(self, universe):
        pass


def test_void():
    strategy = VoidStrategy()
    universe = make_randomwalk()
    strategy.run(universe)

    frame_history = pd.DataFrame(strategy.history)
    frame_transaction = pd.DataFrame(strategy.transaction).set_index('bars')
    frame_wealth = pd.DataFrame(strategy.wealth).set_index('bars')

    assert len(frame_history.index) == 0
    assert (frame_transaction == 0).all(None)
    assert (frame_wealth == 0).all(None)
