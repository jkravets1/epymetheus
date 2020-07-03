import pytest  # noqa: F401

import numpy as np
from epymetheus import Trade


trade_1 = Trade(asset="AAPL", lot=1.0)
trade_2 = Trade(asset=["AAPL", "MSFT"], lot=[1.0, 2.0])


# --------------------------------------------------------------------------------


def test_array_asset():
    trade = trade_1
    array_asset_expected = ["AAPL"]
    assert np.array_equal(trade.array_asset, array_asset_expected)

    trade = trade_2
    array_asset_expected = ["AAPL", "MSFT"]
    assert np.array_equal(trade.array_asset, array_asset_expected)


def test_array_lot():
    trade = trade_1
    array_lot_expected = [1.0]
    assert np.array_equal(trade.array_lot, array_lot_expected)

    trade = trade_2
    array_lot_expected = [1.0, 2.0]
    assert np.array_equal(trade.array_lot, array_lot_expected)


def test_n_orders_1():
    trade = trade_1
    assert trade.n_orders == 1

    trade = trade_2
    assert trade.n_orders == 2
