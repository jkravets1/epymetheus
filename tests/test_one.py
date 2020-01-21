"""
Basic test with a single trade.
"""
import pytest

import pandas as pd
import numpy as np

from epymetheus import Trade, TradeStrategy, Universe
from epymetheus.datasets import make_randomwalk


class OneTradeStrategy(TradeStrategy):
    """Yield one trade."""
    def logic(self, universe, asset, lot, open_bar, close_bar):
        yield Trade(
            asset=asset, lot=lot, open_bar=open_bar, close_bar=close_bar,
        )


def test_one():
    universe = make_randomwalk()

    asset = universe.assets[0]
    lot = 12.3
    open_bar = universe.bars[0]
    close_bar = universe.bars[-1]

    strategy = OneTradeStrategy(
        asset=asset, lot=lot, open_bar=open_bar, close_bar=close_bar,
    )

    strategy.run(universe)

    open_price = universe.prices.at[open_bar, asset]
    close_price = universe.prices.at[close_bar, asset]
    gain = lot * (close_price - open_price)

    assert strategy.history.order_index == np.array([0])
    assert strategy.history.trade_index == np.array([0])
    assert strategy.history.assets == np.array([asset])
    assert strategy.history.lots == np.array([lot])
    assert strategy.history.open_bars == np.array([open_bar])
    assert strategy.history.close_bars == np.array([close_bar])
    assert strategy.history.durations == np.array([close_bar - open_bar])
    assert strategy.history.open_prices == np.array([open_price])
    assert strategy.history.close_prices == np.array([close_price])
    assert strategy.history.gains == np.array([gain])

    # assert strategy.transaction[asset] ==

    # assert strategy.wealth.wealth ==
