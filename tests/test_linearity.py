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
    def logic(self, universe, trades):
        for trade in trades:
            yield trade


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


def make_random_trades(universe, n_trades, seed):
    random_trader = RandomTrader(n_trades=n_trades, seed=seed)
    trades = random_trader.run(universe).trades
    return list(trades)  # for of array is slow


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_add(seed, n_bars, n_assets, n_trades):
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

    # history
    # -------

    history_0 = strategy_0.history
    history_1 = strategy_1.history
    history_A = strategy_A.history

    assert_add(history_0, history_1, history_A, 'asset')
    assert_add(history_0, history_1, history_A, 'lot')
    assert_add(history_0, history_1, history_A, 'open_bars')
    assert_add(history_0, history_1, history_A, 'shut_bars')
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
        assert np.allclose(
            transaction_0[asset] + transaction_1[asset], transaction_A[asset]
        )

    # wealth
    # ------

    wealth_01 = 100 + strategy_0.wealth['wealth'] + strategy_1.wealth['wealth']
    wealth_A = 100 + strategy_A.wealth['wealth']

    assert np.allclose(wealth_01, wealth_A)


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
@pytest.mark.parametrize('a', params_a)
def test_mul(seed, n_bars, n_assets, n_trades, a):
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

    # history
    # -------

    history_1 = strategy_1.history
    history_a = strategy_a.history

    assert_mul(history_1, history_a, 'asset', None)
    assert_mul(history_1, history_a, 'lot', a)
    assert_mul(history_1, history_a, 'open_bars', None)
    assert_mul(history_1, history_a, 'shut_bars', None)
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
