import pytest  # noqa

import numpy as np
import pandas as pd

from epymetheus import Universe, Trade, TradeStrategy
from epymetheus.pipe import (
    trade_index,
    order_index,
    _lot_matrix,
    _value_matrix,
    _opening_matrix,
)

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
    strategy = MockStrategy()
    if universe:
        strategy.universe = universe
    if trades:
        strategy.trades = trades
    return strategy


# --------------------------------------------------------------------------------


def test_trade_trade_index():
    universe = make_universe(100, 3)
    trades = [
        Trade(asset=['Asset0', 'Asset1'], lot=[1, -2], open_bar='Bar0'),
        Trade(asset=['Asset2', 'Asset1'], lot=[3, 4], open_bar='Bar0'),
    ]
    strategy = make_strategy(universe=universe, trades=trades)

    trade_index_expected = np.array([0, 0, 1, 1])

    assert np.equal(trade_index(strategy), trade_index_expected).all()


def test_trade_order_index():
    universe = make_universe(100, 3)
    trades = [
        Trade(asset=['Asset0', 'Asset1'], lot=[1, -2], open_bar='Bar0'),
        Trade(asset=['Asset2', 'Asset1'], lot=[3, 4], open_bar='Bar0'),
    ]
    strategy = make_strategy(universe=universe, trades=trades)

    trade_index_expected = np.array([0, 1, 2, 3])

    assert np.equal(order_index(strategy), trade_index_expected).all()
