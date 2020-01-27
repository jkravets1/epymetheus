import pytest
from ._utils import make_randomuniverse, generate_trades

import random
import pandas as pd
import numpy as np

from epymetheus import Trade, TradeStrategy, Universe


list_seed = [42, 1, 2, 3]
list_n_bars = [10, 1000]
list_n_assets = [1, 100]
list_n_trades = [10]
lots = [0.0, 1, 1.23, -1.0, 123.4, -123.4]


class MultipleTradeStrategy(TradeStrategy):
    """
    Yield multiple trades.

    Parameters
    ----------
    - alocs : list of (asset, lot, open_bar, close_bar)
        Represent trades to yield.
    """
    def logic(self, universe, alocs):
        for aloc in alocs:
            a, l, o, c = aloc
            yield Trade(asset=a, lot=l, open_bar=o, close_bar=c)


def assert_additivity(history_0, history_1, history_A, attribute):
    array_0 = getattr(history_0, attribute)
    array_1 = getattr(history_1, attribute)
    array_A = getattr(history_A, attribute)
    assert np.concatenate([array_0, array_1]).sort() == array_A.sort()


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', list_seed)
@pytest.mark.parametrize('n_bars', list_n_bars)
@pytest.mark.parametrize('n_assets', list_n_assets)
@pytest.mark.parametrize('n_trades', list_n_trades)
def test_add(seed, n_bars, n_assets, n_trades):
    """
    Test additivity of strategies for the following strategies:
        - strategy_0 : yield (trade_00, trade_01, ...)
        - strategy_1 : yield (trade_10, trade_11, ...)
        - strategy_A : yield (trade_00, trade_01, ..., trade_10, trade_11, ...)
    """
    np.random.seed(seed); random.seed(seed)

    universe = make_randomuniverse(n_bars, n_assets)

    trades_0 = list(generate_trades(universe, lots, n_trades))
    trades_1 = list(generate_trades(universe, lots, n_trades))
    trades_A = trades_0 + trades_1

    strategy_0 = MultipleTradeStrategy(alocs=trades_0).run(universe)
    strategy_1 = MultipleTradeStrategy(alocs=trades_1).run(universe)
    strategy_A = MultipleTradeStrategy(alocs=trades_A).run(universe)

    history_0 = strategy_0.history
    history_1 = strategy_1.history
    history_A = strategy_A.history

    assert_additivity(history_0, history_1, history_A, 'assets')
    assert_additivity(history_0, history_1, history_A, 'lots')
    assert_additivity(history_0, history_1, history_A, 'open_bars')
    assert_additivity(history_0, history_1, history_A, 'close_bars')
    assert_additivity(history_0, history_1, history_A, 'durations')
    assert_additivity(history_0, history_1, history_A, 'open_prices')
    assert_additivity(history_0, history_1, history_A, 'close_prices')
    assert_additivity(history_0, history_1, history_A, 'gains')

    # TODO test transaction, wealth


def test_add(seed, n_bars, n_assets, n_trades):
    """
    Test additivity of strategies for the following strategies:
        - strategy_1 : yield (1 * trade_0, 1 * trade_11, ...)
        - strategy_A : yield (A * trade_0, A * trade_01, ...)
    """
    pass
