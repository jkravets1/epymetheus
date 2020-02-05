import pytest  # noqa

import random
import numpy as np
import pandas as pd

from epymetheus import Universe, Trade, TradeStrategy
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader
from epymetheus.pipe.history import (
    trade_index,
    order_index,
    asset_ids,
    lots,
    open_bar_ids,
    shut_bar_ids,
    atakes,
    acuts,
    durations,
    open_prices,
    close_prices,
    gains,
)

params_seed = [42]
params_n_bars = [100, 1000]
params_n_assets = [10, 100]
params_n_trades = [10, 100]


class MockStrategy(TradeStrategy):
    def logic(self, universe):
        pass


def make_strategy(universe=None, trades=None):
    """
    Return strategy with attributes universe and trades.

    Returns
    -------
    strategy : TradeStrategy
    """
    strategy = MockStrategy()
    if universe:
        strategy.universe = universe
    if trades:
        strategy.trades = trades
    return strategy


def make_random_trades(universe, n_trades, seed):
    random_trader = RandomTrader(n_trades=n_trades, seed=seed)
    trades = random_trader.run(universe).trades
    return list(trades)  # for of array is slow


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_index(seed, n_bars, n_assets, n_trades):
    """
    Test trade_id and order_id.
    """
    universe = make_randomwalk(n_bars, n_assets)
    trades = make_random_trades(universe, n_trades, seed)

    trade_index_expected = []
    for i, trade in enumerate(trades):
        trade_index_expected += [i for _ in range(len(trade.asset))]
    order_index_expected = list(range(len(trade_index_expected)))

    strategy = make_strategy(universe=universe, trades=trades)

    assert np.equal(trade_index(strategy), trade_index_expected).all()
    assert np.equal(order_index(strategy), order_index_expected).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_asset_ids(seed, n_bars, n_assets, n_trades):
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomwalk(n_bars, n_assets)
    trades = make_random_trades(universe, n_trades, seed)

    asset_ids_expected = []
    for i, trade in enumerate(trades):
        asset_ids_expected += [int(a[5:]) for a in trade.asset]  # Asset name is 'Asset{i}'

    strategy = make_strategy(universe=universe, trades=trades)

    assert np.equal(asset_ids(strategy), asset_ids_expected).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_lots(seed, n_bars, n_assets, n_trades):
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomwalk(n_bars, n_assets)
    trades = make_random_trades(universe, n_trades, seed)

    expected = []
    for i, trade in enumerate(trades):
        expected += [lot for lot in trade.lot]  # Asset name is 'Asset{i}'

    strategy = make_strategy(universe=universe, trades=trades)

    assert np.equal(lots(strategy), expected).all()
