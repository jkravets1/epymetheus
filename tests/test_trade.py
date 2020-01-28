import pytest

from random import choice, choices
from epymetheus import Trade


lots = [0.0, 1, 1.23, -1.23, 123.4, -123.4]

list_n_orders = [1, 5]
list_a = [0.0, 1, 1.23, -1.23, 123.4, -123.4]


def make_trade(n_orders):
    if n_orders == 1:
        asset = 'asset0'
        lot = choice(lots)
    else:
        asset=[f'asset{i}' for i in range(n_orders)],
        lot=choices(lots, k=n_orders)
    return Trade(
        asset=asset, open_bar='bar0', close_bar='bar1', lot=lot,
    )


def assert_trade_operation(trade0, trade1, operator):
    assert trade1.asset == trade0.asset
    assert trade1.open_bar == trade0.open_bar
    assert trade1.close_bar == trade0.close_bar
    if hasattr(trade1.lot, '__iter__'):
        assert trade1.lot == [operator(lot) for lot in trade0.lot]
    else:
        assert trade1.lot == operator(trade0.lot)


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('n_orders', list_n_orders)
def test_n_orders(n_orders):
    trade0 = make_trade(n_orders)
    assert trade0.n_orders == n_orders


@pytest.mark.parametrize('n_orders', list_n_orders)
@pytest.mark.parametrize('a', list_a)
def test_mul(n_orders, a):
    trade0 = make_trade(n_orders)
    trade1 = a * trade0
    assert_trade_operation(trade0, trade1, lambda x: a * x)


@pytest.mark.parametrize('n_orders', list_n_orders)
@pytest.mark.parametrize('a', list_a)
def test_rmul(n_orders, a):
    trade0 = make_trade(n_orders)
    trade1 = trade0 * a
    assert_trade_operation(trade0, trade1, lambda x: a * x)


@pytest.mark.parametrize('n_orders', list_n_orders)
def test_neg(n_orders):
    trade0 = make_trade(n_orders)
    trade1 = - trade0
    assert_trade_operation(trade0, trade1, lambda x: -x)


@pytest.mark.parametrize('n_orders', list_n_orders)
@pytest.mark.parametrize('a', list_a)
def test_truediv(n_orders, a):
    trade0 = make_trade(n_orders)

    if a != 0:
        trade1 = trade0 / a
        assert_trade_operation(trade0, trade1, lambda x: x / a)
    else:
        with pytest.raises(ZeroDivisionError):
            trade1 = trade0 / a


@pytest.mark.parametrize('n_orders', list_n_orders)
@pytest.mark.parametrize('a', list_a)
def test_floordiv(n_orders, a):
    trade0 = make_trade(n_orders)

    if a != 0:
        trade1 = trade0 // a
        assert_trade_operation(trade0, trade1, lambda x: x // a)
    else:
        with pytest.raises(ZeroDivisionError):
            trade1 = trade0 // a
