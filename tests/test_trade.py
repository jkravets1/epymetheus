import pytest

import numpy as np
from random import choice, choices
from epymetheus import Trade


lots = [0.0, 1, 1.23, -1.23, 123.4, -123.4]

params_n_orders = [1, 5]
params_a = [0.0, 1, 1.23, -1.23, 123.4, -123.4]


def make_trade(n_orders):
    if n_orders == 1:
        asset = 'asset0'
        lot = choice(lots)
    else:
        asset = [f'asset{i}' for i in range(n_orders)],
        lot = choices(lots, k=n_orders)
    return Trade(
        asset=asset, open_bar='bar0', close_bar='bar1', lot=lot,
    )


def assert_trade_operation(trade0, trade1, operator):
    """
    Examples
    --------
    >>> trade0 = Trade(..., lot=[1.0, -2.0], ...)
    >>> trade1 = Trade(..., lot=[2.0, -4.0], ...)
    >>> operator = lambda x: 2 * x
    >>> assert_trade_operation(trade0, trade1, operator)
    # True; no AssertionError
    """
    lot = np.array([operator(x) for x in trade0.lot])
    trade0.lot = lot
    assert trade0 == trade1


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('n_orders', params_n_orders)
def test_n_orders(n_orders):
    trade0 = make_trade(n_orders)
    assert trade0.n_orders == n_orders


@pytest.mark.parametrize('n_orders', params_n_orders)
@pytest.mark.parametrize('a', params_a)
def test_mul(n_orders, a):
    trade0 = make_trade(n_orders)
    trade1 = a * trade0
    print(type(trade0.lot))
    print(type(trade1.lot))
    assert_trade_operation(trade0, trade1, lambda x: a * x)


@pytest.mark.parametrize('n_orders', params_n_orders)
@pytest.mark.parametrize('a', params_a)
def test_rmul(n_orders, a):
    trade0 = make_trade(n_orders)
    trade1 = trade0 * a
    assert_trade_operation(trade0, trade1, lambda x: a * x)


@pytest.mark.parametrize('n_orders', params_n_orders)
def test_neg(n_orders):
    trade0 = make_trade(n_orders)
    trade1 = - trade0
    assert_trade_operation(trade0, trade1, lambda x: -x)


@pytest.mark.parametrize('n_orders', params_n_orders)
@pytest.mark.parametrize('a', params_a)
def test_truediv(n_orders, a):
    trade0 = make_trade(n_orders)

    if a != 0:
        trade1 = trade0 / a
        assert_trade_operation(trade0, trade1, lambda x: x / a)
    else:
        with pytest.raises(ZeroDivisionError):
            trade1 = trade0 / a


# @pytest.mark.parametrize('n_orders', params_n_orders)
# @pytest.mark.parametrize('a', params_a)
# def test_floordiv(n_orders, a):
#     trade0 = make_trade(n_orders)

#     if a != 0:
#         trade1 = trade0 // a
#         assert_trade_operation(trade0, trade1, lambda x: x // a)
#     else:
#         print(trade0.lot)
#         with pytest.raises(ZeroDivisionError):
#             trade1 = trade0 // a
