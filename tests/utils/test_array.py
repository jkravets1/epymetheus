import pytest  # noqa: F401

import numpy as np

from epymetheus.utils.array import catch_first_index


# params_seed = [42, 1, 2, 3]
# params_n_samples = [10, 100, 1000]
# params_n_series = [1, 10, 100]


# def make_sin(n_samples, n_series, period, shift):
#     x = row(shape=(n_samples, n_series)) + shift.reshape(1, -1)
#     return np.sin(2 * np.pi * x / period)


# --------------------------------------------------------------------------------


def test_catch_first_index():
    a = np.array([0, 1, 0, 1]).astype(bool)
    i_expected = 1
    assert catch_first_index(a) == i_expected

    a = np.array([1, 0, 1, 0]).astype(bool)
    i_expected = 0
    assert catch_first_index(a) == i_expected

    a = np.array([0, 0, 0, 0]).astype(bool)
    i_expected = -1
    assert catch_first_index(a) == i_expected


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_samples', params_n_samples)
# @pytest.mark.parametrize('n_series', params_n_series)
# def test_true_since(seed, n_samples, n_series):
#     np.random.seed(seed)
#     index = np.random.randint(n_samples, size=n_series)

#     array = true_since(index, n_samples=n_samples)

#     for i in range(n_series):
#         assert (~array[:index[i], i]).all()
#         assert array[index[i]:, i].all()


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_samples', params_n_samples)
# @pytest.mark.parametrize('n_series', params_n_series)
# def test_true_until(seed, n_samples, n_series):
#     np.random.seed(seed)
#     index = np.random.randint(n_samples, size=n_series)

#     array = true_until(index, n_samples=n_samples)
#     for i in range(n_series):
#         assert array[:index[i] + 1, i].all()
#         assert (~array[index[i] + 1:, i]).all()


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_samples', params_n_samples)
# @pytest.mark.parametrize('n_series', params_n_series)
# def test_true_at(seed, n_samples, n_series):
#     np.random.seed(seed)
#     index = np.random.randint(n_samples, size=n_series)

#     array = true_at(index, n_samples=n_samples)
#     for i in range(n_series):
#         assert array[index[i], i]
#         assert (~array[:index[i], i]).all()
#         assert (~array[index[i] + 1:, i]).all()


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_samples', params_n_samples)
# @pytest.mark.parametrize('n_series', params_n_series)
# def test_row(seed, n_samples, n_series):
#     np.random.seed(seed)

#     array = row((n_samples, n_series))
#     for i in range(n_series):
#         assert (array[:, i] == np.arange(n_samples)).all()


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_samples', params_n_samples)
# @pytest.mark.parametrize('n_series', params_n_series)
# def test_cross_up(seed, n_samples, n_series):
#     period = n_samples // 10
#     shift = np.random.randint(period, size=n_series)

#     array = make_sin(n_samples, n_series, period, shift)

#     signal = cross_up(array)

#     x = row((n_samples, n_series)) + shift
#     signal_expected = (x % period == 1)
#     signal_expected[0, :] = False

#     assert (signal == signal_expected).all()


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_samples', params_n_samples)
# @pytest.mark.parametrize('n_series', params_n_series)
# def test_cross_down(seed, n_samples, n_series):
#     period = n_samples // 10
#     shift = np.random.randint(period, size=n_series)

#     array = - make_sin(n_samples, n_series, period, shift)

#     signal = cross_down(array)

#     x = row((n_samples, n_series)) + shift
#     signal_expected = (x % period == 1)
#     signal_expected[0, :] = False
#     print(np.concatenate([signal, signal_expected], axis=1))

#     assert (signal == signal_expected).all()
