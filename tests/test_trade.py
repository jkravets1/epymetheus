import pytest

from epymetheus import Trade


list_lot = [0.0, 1, 1.23, -1.23, 123.4, -123.4]
list_a = [0.0, 1, 1.23, -1.23, 123.4, -123.4]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('lot', list_lot)
@pytest.mark.parametrize('a', list_a)
def test_mul(lot, a):
    trade = Trade(asset='asset0', open_bar='bar0', close_bar='bar1', lot=lot)
    trade_mul = a * trade

    assert trade_mul.asset == trade.asset
    assert trade_mul.open_bar == trade.open_bar
    assert trade_mul.close_bar == trade.close_bar
    assert trade_mul.lot == a * trade.lot


@pytest.mark.parametrize('lot', list_lot)
@pytest.mark.parametrize('a', list_a)
def test_rmul(lot, a):
    trade = Trade(asset='asset0', open_bar='bar0', close_bar='bar1', lot=lot)
    trade_mul = trade * a

    assert trade_mul.asset == trade.asset
    assert trade_mul.open_bar == trade.open_bar
    assert trade_mul.close_bar == trade.close_bar
    assert trade_mul.lot == a * trade.lot


@pytest.mark.parametrize('lot', list_lot)
def test_neg(lot):
    trade = Trade(asset='asset0', open_bar='bar0', close_bar='bar1', lot=lot)
    trade_mul = - trade

    assert trade_mul.asset == trade.asset
    assert trade_mul.open_bar == trade.open_bar
    assert trade_mul.close_bar == trade.close_bar
    assert trade_mul.lot == (-1) * trade.lot
