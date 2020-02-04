import pytest


from epymetheus.utils.bunch import Bunch


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
        print(bunch.d)
