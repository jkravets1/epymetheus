import pytest

import random
import numpy as np

from epymetheus import Trade, TradeStrategy
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader


params_seed = [42]
params_n_bars = [10, 1000]
params_n_assets = [10, 100]
params_n_trades = [10, 100]
params_a = [1.23, -1.23]

lots = [0.0, 1, 1.23, -1.23, 12345.678]


class MultipleTradeStrategy(TradeStrategy):
    """
    Yield multiple trades.

    Parameters
    ----------
    trades : iterable of Trade
    """
    def __init__(self, trades):
        self.trades = trades

    def logic(self, universe):
        for trade in self.trades:
            yield trade


def make_random_trades(universe, n_trades, seed):
    random_trader = RandomTrader(n_trades=n_trades, seed=seed)
    trades = random_trader.run(universe).trades
    return list(trades)  # for of array is slow


def assert_add(history_0, history_1, history_A, attribute):
    array_0 = getattr(history_0, attribute)
    array_1 = getattr(history_1, attribute)
    array_A = getattr(history_A, attribute)
    array_01 = np.sort(np.concatenate([array_0, array_1]))
    assert np.equal(array_01, np.sort(array_A)).all()


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


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_linearity_add(seed, n_bars, n_assets, n_trades):
    """
    Test additivity of strategies for the following strategies:
        - strategy_0 : yield (trade_00, trade_01, ...)
        - strategy_1 : yield (trade_10, trade_11, ...)
        - strategy_A : yield (trade_00, trade_01, ..., trade_10, trade_11, ...)
    """
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomwalk(n_bars, n_assets)

    trades_0 = make_random_trades(universe, n_trades, seed + 0)
    trades_1 = make_random_trades(universe, n_trades, seed + 1)
    trades_A = trades_0 + trades_1

    strategy_0 = MultipleTradeStrategy(trades=trades_0).run(universe)
    strategy_1 = MultipleTradeStrategy(trades=trades_1).run(universe)
    strategy_A = MultipleTradeStrategy(trades=trades_A).run(universe)

    history_0 = strategy_0.history
    history_1 = strategy_1.history
    history_A = strategy_A.history

    for attr in (
        'asset',
        'lot',
        'open_bars',
        'shut_bars',
        'durations',
        'open_prices',
        'close_prices',
        'gains',
    ):
        assert_add(history_0, history_1, history_A, attr)


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
@pytest.mark.parametrize('a', params_a)
def test_linearity_mul(seed, n_bars, n_assets, n_trades, a):
    """
    Test additivity of strategies for the following strategies:
        - strategy_1 : yield (1 * trade_0, 1 * trade_11, ...)
        - strategy_a : yield (a * trade_0, a * trade_01, ...)
    """
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomwalk(n_bars, n_assets)

    trades_1 = make_random_trades(universe, n_trades, seed + 1)
    trades_a = [
        Trade(
            asset=trade.asset,
            lot=a * trade.lot,
            open_bar=trade.open_bar,
            shut_bar=trade.shut_bar
        )
        for trade in trades_1
    ]

    strategy_1 = MultipleTradeStrategy(trades=trades_1).run(universe)
    strategy_a = MultipleTradeStrategy(trades=trades_a).run(universe)

    history_1 = strategy_1.history
    history_a = strategy_a.history

    for attr in (
        'asset',
        'open_bars',
        'shut_bars',
        'durations',
        'open_prices',
        'close_prices',
    ):
        assert_mul(history_1, history_a, attr, None)

    for attr in ('lot', 'gains'):
        assert_mul(history_1, history_a, attr, a)
