import pytest

import numpy as np

from epymetheus import Universe
from epymetheus.datasets import make_randomwalk

params_n_bars = [10, 1000]
params_n_assets = [1, 100]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_error_nan(n_bars, n_assets):
    """
    Universe should raise ValueError when `universe.prices`
    contains `numpy.nan`.
    """
    prices = make_randomwalk(n_bars, n_assets).prices
    prices.iat[n_bars // 2, n_assets // 2] = np.nan

    with pytest.raises(ValueError):
        universe = Universe(prices)  # noqa: F841


@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_error_inf(n_bars, n_assets):
    """
    Universe should raise ValueError when `universe.prices`
    contains `numpy.inf`.
    """
    prices = make_randomwalk(n_bars, n_assets).prices
    prices.iat[n_bars // 2, n_assets // 2] = np.inf

    with pytest.raises(ValueError):
        universe = Universe(prices)  # noqa: F841


# @pytest.mark.parametrize('n_bars', params_n_bars)
# @pytest.mark.parametrize('n_assets', params_n_assets)
# def test_error_inf(n_bars, n_assets):
#     """
#     Universe should raise ValueError when `universe.prices`
#     contains `pandas.NA`.
#     """
#     prices = make_randomwalk(n_bars, n_assets).prices
#     prices.iat[n_bars // 2, n_assets // 2] = pd.NA

#     with pytest.raises(ValueError):
#         universe = Universe(prices)
#         print(universe)


@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_error_nonunique_bar(n_bars, n_assets):
    bars = [f'MyBar{i}' for i in range(n_bars)]
    bars[n_bars // 2] = 'MyBar0'

    prices = make_randomwalk(n_bars, n_assets).prices
    prices.index = bars

    with pytest.raises(ValueError):
        universe = Universe(prices)  # noqa: F841


@pytest.mark.parametrize('n_bars', params_n_bars[-1:])
@pytest.mark.parametrize('n_assets', params_n_assets[-1:])
def test_error_nonunique_assets(n_bars, n_assets):
    assets = [f'MyAsset{i}' for i in range(n_assets)]
    assets[n_assets // 2] = 'MyAsset0'
    print(assets)

    prices = make_randomwalk(n_bars, n_assets).prices
    prices.columns = assets

    with pytest.raises(ValueError):
        universe = Universe(prices)  # noqa: F841
