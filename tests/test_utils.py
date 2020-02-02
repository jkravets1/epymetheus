import pytest

import numpy as np

from epymetheus.utils import Bunch
# from epymetheus.utils import check_prices



def test_bunch():
    bunch = Bunch(a='value_a')
    bunch['b'] = 'value_b'
    bunch.c = 'value_c'

    assert bunch.a == 'value_a'
    assert bunch.b == 'value_b'
    assert bunch.c == 'value_c'
    assert bunch['a'] == 'value_a'
    assert bunch['b'] == 'value_b'
    assert bunch['c'] == 'value_c'

    assert dir(bunch) == ['a', 'b', 'c']

    with pytest.raises(AttributeError):
        d = bunch.d


# @pytest.mark.parametrize('invalid_value', [np.nan, np.inf])
# def test_check_prices(invalid_value):
#     prices = np.random.randn(100, 100)
#     prices[42, 24] = invalid_value

#     with pytest.raises(ValueError):
#         check_prices(prices)
