import pytest  # noqa

import numpy as np
import pandas as pd

from epymetheus import Universe, Trade, TradeStrategy
from epymetheus.pipe.wealth import (
    wealth,
)


# TODO this is just tentative; add multiple and robust tests


def make_universe(n_bars, n_assets, pricedata=None):
    if pricedata is None:
        pricedata = np.zeros((n_bars, n_assets))
    prices = pd.DataFrame(
        pricedata,
        # index=[f'Bar{i}' for i in range(n_bars)],
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
        # strategy.trades = trades
        def logic(*args, **kwargs):
            for trade in trades:
                yield trade
        strategy.logic = logic
    return strategy


# --------------------------------------------------------------------------------


def test_wealth():
    universe = make_universe(5, 3)
    prices = pd.DataFrame([
        [1., 10., 100.],
        [2., 20., 200.],
        [4., 40., 400.],
        [7., 70., 700.],
        [10, 100, 1000],
    ], index=universe.bars, columns=universe.assets)
    universe.prices = prices

    trades = [
        Trade(asset=['Asset0', 'Asset1'], lot=[1, -2], open_bar=0, shut_bar=2),
        Trade(asset='Asset2', lot=3, open_bar=1, shut_bar=4),
    ]
    strategy = make_strategy(universe=universe, trades=trades).run(universe)

    # transaction = np.array([
    #     [1, -2, 0],
    #     [0, 0, 3],
    #     [-1, 2, 0],
    #     [0, 0, 0],
    #     [0, 0, -3],
    # ])

    # position = np.concatenate([
    #     np.zeros((1, strategy.universe.n_assets)),
    #     np.cumsum(strategy.transaction_matrix, axis=0)[:-1, :],
    # ], axis=0)

    # w1 = np.array([0, 1, 3, 3, 3])
    # w2 = (-2) * np.array([0, 10, 30, 30, 30])
    # w3 = 3 * np.array([0, 0, 200, 500, 800])
    # expected = w1 + w2 + w3

    # price_change = np.diff(
    #     strategy.universe.prices.values,
    #     axis=0, prepend=0,
    # )

    # a = np.cumsum(
    #     np.sum(position * price_change, axis=1),
    #     axis=0,
    # )
    # print('position', position)
    # print('price change', price_change)
    # print('wealth', a)
    # print('wealth expected', expected)

    # assert np.equal(wealth(strategy), expected).all()
    assert np.equal(a, expected).all()
