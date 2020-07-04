import pytest  # noqa: F401

import numpy as np
from epymetheus import Trade
from epymetheus.datasets import make_randomwalk


class TestIsExecuted:
    """
    Test `Trade.is_executed`.
    """

    trade0 = Trade(asset="A0", lot=1.0)

    def test_value(self):
        trade = self.trade0
        assert not trade.is_executed
        trade = trade.execute(make_randomwalk(seed=42))
        assert trade.is_executed


class TestArrayAsset:
    """
    Test `Trade.array_asset`.
    """

    trade0 = Trade(asset="A0", lot=1.0)
    trade1 = Trade(asset=["A0", "A1"], lot=[2.0, 3.0])

    @pytest.mark.parametrize(
        "trade, expected", [(trade0, ["A0"]), (trade1, ["A0", "A1"])]
    )
    def test_value(self, trade, expected):
        assert isinstance(trade.array_asset, np.ndarray)
        assert np.array_equal(trade.array_asset, expected)


class TestArrayLot:
    """
    Test `Trade.array_lot`.
    """

    trade0 = Trade(asset="A0", lot=1.0)
    trade1 = Trade(asset=["A0", "A1"], lot=[2.0, 3.0])

    @pytest.mark.parametrize("trade, expected", [(trade0, [1.0]), (trade1, [2.0, 3.0])])
    def test_value(self, trade, expected):
        assert isinstance(trade.array_lot, np.ndarray)
        assert np.array_equal(trade.array_lot, expected)


class TestNOrders:
    """
    Test `Trade.n_orders`.
    """

    trade0 = Trade(asset="A0", lot=1.0)
    trade1 = Trade(asset=["A0", "A1"], lot=[2.0, 3.0])

    @pytest.mark.parametrize("trade, expected", [(trade0, 1), (trade1, 2)])
    def test_value(self, trade, expected):
        assert trade.n_orders == expected
