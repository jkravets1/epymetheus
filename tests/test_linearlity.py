import pytest
from ._utils import make_randomuniverse, generate_trades

import random
import numpy as np

from epymetheus import Trade, TradeStrategy


list_seed = [42, 1, 2, 3]
list_n_bars = [10, 1000]
list_n_assets = [1, 100]
list_n_trades = [10]
list_a = [1.23, -1.23]

lots = [0.0, 1, 1.23, -1.23, 12345.678]


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


def assert_add(history_0, history_1, history_A, attribute):
    array_0 = getattr(history_0, attribute)
    array_1 = getattr(history_1, attribute)
    array_A = getattr(history_A, attribute)
    assert np.concatenate([array_0, array_1]).sort() == array_A.sort()


def assert_mul(history_1, history_a, attribute, a=None):
    array_1 = getattr(history_1, attribute)
    array_a = getattr(history_a, attribute)
    if a is not None:
        array_1 *= float(a)

    print(array_1, array_1.dtype)
    print(array_a, array_a.dtype)

    if array_1.dtype == np.float64:
        assert np.allclose(array_1, array_a)
    else:
        assert (array_1 == array_a).all()


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
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomuniverse(n_bars, n_assets)

    trades_0 = list(generate_trades(universe, lots, n_trades))
    trades_1 = list(generate_trades(universe, lots, n_trades))
    trades_A = trades_0 + trades_1

    strategy_0 = MultipleTradeStrategy(alocs=trades_0).run(universe)
    strategy_1 = MultipleTradeStrategy(alocs=trades_1).run(universe)
    strategy_A = MultipleTradeStrategy(alocs=trades_A).run(universe)

    # history
    # -------

    history_0 = strategy_0.history
    history_1 = strategy_1.history
    history_A = strategy_A.history

    assert_add(history_0, history_1, history_A, 'assets')
    assert_add(history_0, history_1, history_A, 'lots')
    assert_add(history_0, history_1, history_A, 'open_bars')
    assert_add(history_0, history_1, history_A, 'close_bars')
    assert_add(history_0, history_1, history_A, 'durations')
    assert_add(history_0, history_1, history_A, 'open_prices')
    assert_add(history_0, history_1, history_A, 'close_prices')
    assert_add(history_0, history_1, history_A, 'gains')

    # transaction
    # -----------

    transaction_0 = strategy_0.transaction
    transaction_1 = strategy_1.transaction
    transaction_A = strategy_A.transaction

    for asset in universe.assets:
        assert_add(transaction_0, transaction_1, transaction_A, asset)

    # wealth
    # ------

    wealth_0 = strategy_0.wealth
    wealth_1 = strategy_1.wealth
    wealth_A = strategy_A.wealth

    assert_add(wealth_0, wealth_1, wealth_A, 'wealth')


@pytest.mark.parametrize('seed', list_seed)
@pytest.mark.parametrize('n_bars', list_n_bars)
@pytest.mark.parametrize('n_assets', list_n_assets)
@pytest.mark.parametrize('n_trades', list_n_trades)
@pytest.mark.parametrize('a', list_a)
def test_mul(seed, n_bars, n_assets, n_trades, a):
    """
    Test additivity of strategies for the following strategies:
        - strategy_1 : yield (1 * trade_0, 1 * trade_11, ...)
        - strategy_a : yield (a * trade_0, a * trade_01, ...)
    """
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomuniverse(n_bars, n_assets)

    trades_1 = list(generate_trades(universe, lots, n_trades))
    trades_a = [(asset, a * lot, open_bar, close_bar)
                for asset, lot, open_bar, close_bar in trades_1]

    strategy_1 = MultipleTradeStrategy(alocs=trades_1).run(universe)
    strategy_a = MultipleTradeStrategy(alocs=trades_a).run(universe)

    # history
    # -------

    history_1 = strategy_1.history
    history_a = strategy_a.history

    assert_mul(history_1, history_a, 'assets', None)
    assert_mul(history_1, history_a, 'lots', a)
    assert_mul(history_1, history_a, 'open_bars', None)
    assert_mul(history_1, history_a, 'close_bars', None)
    assert_mul(history_1, history_a, 'durations', None)
    assert_mul(history_1, history_a, 'open_prices', None)
    assert_mul(history_1, history_a, 'close_prices', None)
    assert_mul(history_1, history_a, 'gains', a)

    # transaction
    # -----------

    transaction_1 = strategy_1.transaction
    transaction_a = strategy_a.transaction

    for asset in universe.assets:
        assert_mul(transaction_1, transaction_a, asset, a)

    # wealth
    # ------

    wealth_1 = strategy_1.wealth
    wealth_a = strategy_a.wealth

    assert_mul(wealth_1, wealth_a, 'wealth', a)
