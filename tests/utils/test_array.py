import pytest

import numpy as np

from epymetheus.utils.array import (
    true_since,
    true_until,
    true_at,
    row,
    cross_up,
    cross_down,
    catch_first,
)

params_seed = [42, 1, 2, 3]
params_n_samples = [10, 100, 1000]
params_n_series = [1, 10, 100]


def make_sin(n_samples, n_series, period, shift):
    x = row(shape=(n_samples, n_series)) + shift.reshape(1, -1)
    return np.sin(2 * np.pi * x / period)


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_samples', params_n_samples)
@pytest.mark.parametrize('n_series', params_n_series)
def test_true_since(seed, n_samples, n_series):
    np.random.seed(seed)
    index = np.random.randint(n_samples, size=n_series)

    array = true_since(index, n_samples=n_samples)

    for i in range(n_series):
        assert (~array[:index[i], i]).all()
        assert array[index[i]:, i].all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_samples', params_n_samples)
@pytest.mark.parametrize('n_series', params_n_series)
def test_true_until(seed, n_samples, n_series):
    np.random.seed(seed)
    index = np.random.randint(n_samples, size=n_series)

    array = true_until(index, n_samples=n_samples)
    for i in range(n_series):
        assert array[:index[i] + 1, i].all()
        assert (~array[index[i] + 1:, i]).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_samples', params_n_samples)
@pytest.mark.parametrize('n_series', params_n_series)
def test_true_at(seed, n_samples, n_series):
    np.random.seed(seed)
    index = np.random.randint(n_samples, size=n_series)

    array = true_at(index, n_samples=n_samples)
    for i in range(n_series):
        assert array[index[i], i]
        assert (~array[:index[i], i]).all()
        assert (~array[index[i] + 1:, i]).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_samples', params_n_samples)
@pytest.mark.parametrize('n_series', params_n_series)
def test_row(seed, n_samples, n_series):
    np.random.seed(seed)

    array = row((n_samples, n_series))
    for i in range(n_series):
        assert (array[:, i] == np.arange(n_samples)).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_samples', params_n_samples)
@pytest.mark.parametrize('n_series', params_n_series)
def test_cross_up(seed, n_samples, n_series):
    period = n_samples // 10
    shift = np.random.randint(period, size=n_series)

    array = make_sin(n_samples, n_series, period, shift)

    signal = cross_up(array)

    x = row((n_samples, n_series)) + shift
    signal_expected = (x % period == 1)
    signal_expected[0, :] = False

    assert (signal == signal_expected).all()


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_samples', params_n_samples)
@pytest.mark.parametrize('n_series', params_n_series)
def test_cross_down(seed, n_samples, n_series):
    period = n_samples // 10
    shift = np.random.randint(period, size=n_series)

    array = - make_sin(n_samples, n_series, period, shift)

    signal = cross_down(array)

    x = row((n_samples, n_series)) + shift
    signal_expected = (x % period == 1)
    signal_expected[0, :] = False
    print(np.concatenate([signal, signal_expected], axis=1))

    assert (signal == signal_expected).all()


def test_catch_first():
    a = np.array([
        [True, False, False],
        [False, True, False],
        [True, False, False]
    ])
    b = np.array([
        [False, True, False],
        [False, False, True],
        [True, False, False],
    ])
    signal = catch_first([a, b])
    signal_expected = np.array([0, 0, 1])

    assert (signal == signal_expected).all()
