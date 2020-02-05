import pytest  # noqa

import random
import numpy as np
import pandas as pd

from epymetheus import Universe, Trade, TradeStrategy
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
params_n_assets = [10, 100]  # >= 5
params_n_trades = [10, 100]


def make_universe(n_bars, n_assets, pricedata=None):
    if pricedata is None:
        pricedata = np.zeros((n_bars, n_assets))
    prices = pd.DataFrame(
        pricedata,
        index=[f'Bar{i}' for i in range(n_bars)],
        columns=[f'Asset{i}' for i in range(n_assets)],
    )
    return Universe(prices)


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




# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_index(seed, n_bars, n_assets, n_trades, generate_trades):
    """
    Test trade_id and order_id.
    """
    np.random.seed(seed)
    random.seed(seed)

    universe = make_universe(n_bars, n_assets)

    trades = []
    trade_index_expected = []
    for i, trade in enumerate(generate_trades(universe, n_trades)):
        trade_index_expected += [i for _ in range(len(trade.asset))]
        trades.append(trade)
    order_index_expected = list(range(len(trade_index_expected)))

    strategy = make_strategy(universe=universe, trades=trades)

    assert np.equal(trade_index(strategy), trade_index_expected).all()
    assert np.equal(order_index(strategy), order_index_expected).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_asset_ids(seed, n_bars, n_assets, n_trades, generate_trades):
    np.random.seed(seed)
    random.seed(seed)

    universe = make_universe(n_bars, n_assets)

    trades = []
    asset_ids_expected = []
    for i, trade in enumerate(generate_trades(universe, n_trades)):
        asset_ids_expected += [int(a[5:]) for a in trade.asset]  # Asset name is 'Asset{i}'
        trades.append(trade)

    strategy = make_strategy(universe=universe, trades=trades)

    assert np.equal(asset_ids(strategy), asset_ids_expected).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('n_trades', params_n_trades)
def test_lots(seed, n_bars, n_assets, n_trades, generate_trades):
    np.random.seed(seed)
    random.seed(seed)

    universe = make_universe(n_bars, n_assets)

    trades = []
    expected = []
    for i, trade in enumerate(generate_trades(universe, n_trades)):
        expected += [lot for lot in trade.lot]  # Asset name is 'Asset{i}'
        trades.append(trade)

    strategy = make_strategy(universe=universe, trades=trades)

    assert np.equal(lots(strategy), expected).all()
