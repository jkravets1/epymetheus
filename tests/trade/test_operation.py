import pytest

from itertools import cycle, islice

import numpy as np
from random import choice, choices
from epymetheus import Trade


def yield_trades(n_orders):
    """
    Examples
    --------
    >>> for trade in yield_trades(1):
    ...     print(trade)
    Trade(asset='A0', open_bar='B0', shut_bar='B1', lot=0.0, take=1.0, stop=-1.0)
    Trade(asset='A0', open_bar='B0', shut_bar='B1', lot=1, take=1.0, stop=-1.0)
    Trade(asset='A0', open_bar='B0', shut_bar='B1', lot=1.23, take=1.0, stop=-1.0)
    Trade(asset='A0', open_bar='B0', shut_bar='B1', lot=-1.23, take=1.0, stop=-1.0)
    Trade(asset='A0', open_bar='B0', shut_bar='B1', lot=123.4, take=1.0, stop=-1.0)
    Trade(asset='A0', open_bar='B0', shut_bar='B1', lot=-123.4, take=1.0, stop=-1.0)
    >>> for trade in yield_trades(2):
    ...     print(trade)
    Trade(asset=['A0', 'A1'], open_bar='B0', shut_bar='B1', lot=[0.0, 1], take=1.0, stop=-1.0)
    Trade(asset=['A0', 'A1'], open_bar='B0', shut_bar='B1', lot=[1, 1.23], take=1.0, stop=-1.0)
    Trade(asset=['A0', 'A1'], open_bar='B0', shut_bar='B1', lot=[1.23, -1.23], take=1.0, stop=-1.0)
    Trade(asset=['A0', 'A1'], open_bar='B0', shut_bar='B1', lot=[-1.23, 123.4], take=1.0, stop=-1.0)
    Trade(asset=['A0', 'A1'], open_bar='B0', shut_bar='B1', lot=[123.4, -123.4], take=1.0, stop=-1.0)
    Trade(asset=['A0', 'A1'], open_bar='B0', shut_bar='B1', lot=[-123.4, 0.0], take=1.0, stop=-1.0)
    """
    params_lot = [0.0, 1, 1.23, -1.23, 123.4, -123.4]

    if n_orders == 1:
        for lot in params_lot:
            yield Trade(
                asset="A0", open_bar="B0", shut_bar="B1", lot=lot, take=1.0, stop=-1.0,
            )
    else:
        for i, _ in enumerate(params_lot):
            asset = [f"A{i}" for i in range(n_orders)]
            lot = list(islice(cycle(params_lot), i, i + n_orders))
            yield Trade(
                asset=asset, open_bar="B0", shut_bar="B1", lot=lot, take=1.0, stop=-1.0,
            )


params_trade = list(yield_trades(1)) + list(yield_trades(2))
params_a = [0.0, 1, 1.23, -1.23, 123.4, -123.4]


def assert_trade_operation(trade0, trade1, operator):
    """
    Examples
    --------
    >>> trade0 = Trade(asset=['asset0', 'asset1'], lot=[1.0, -2.0])
    >>> trade1 = Trade(asset=['asset0', 'asset1'], lot=[2.0, -4.0])
    >>> operator = lambda x: 2 * x
    >>> assert_trade_operation(trade0, trade1, operator)  # No Error
    """
    assert trade0.asset == trade1.asset
    assert trade0.open_bar == trade1.open_bar
    assert trade0.shut_bar == trade1.shut_bar
    assert np.allclose([operator(x) for x in trade0.array_lot], trade1.array_lot)
    assert trade0.take == trade1.take
    assert trade0.stop == trade1.stop


# --------------------------------------------------------------------------------


class TestOperation:
    @pytest.mark.parametrize("trade0", params_trade)
    @pytest.mark.parametrize("a", params_a)
    def test_mul(self, trade0, a):
        print(trade0)
        trade1 = a * trade0
        assert_trade_operation(trade0, trade1, lambda x: a * x)

    @pytest.mark.parametrize("trade0", params_trade)
    @pytest.mark.parametrize("a", params_a)
    def test_rmul(self, trade0, a):
        trade1 = trade0 * a
        assert_trade_operation(trade0, trade1, lambda x: a * x)

    @pytest.mark.parametrize("trade0", params_trade)
    def test_neg(self, trade0):
        trade1 = -trade0
        assert_trade_operation(trade0, trade1, lambda x: -x)

    @pytest.mark.parametrize("trade0", params_trade)
    @pytest.mark.parametrize("a", params_a)
    def test_truediv(self, trade0, a):
        if a != 0:
            trade1 = trade0 / a
            assert_trade_operation(trade0, trade1, lambda x: x / a)
        else:
            with pytest.raises(ZeroDivisionError):
                trade1 = trade0 / a


if __name__ == "__main__":
    from doctest import testmod

    testmod()
