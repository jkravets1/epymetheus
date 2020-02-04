import pytest
from ._utils import make_randomuniverse

import random
import numpy as np

from epymetheus import Universe


params_seed = [42]
params_n_bars = [10, 1000]
params_n_assets = [1, 100]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_assets(seed, n_bars, n_assets):
    """
    Tests n_bars, n_assets, bars, assets.
    """
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomuniverse(n_bars, n_assets)

    assert universe.n_bars == n_bars
    assert universe.n_assets == n_assets

    new_bars = [f'newbar{i}' for i in range(n_bars)]
    new_assets = [f'newasset{i}' for i in range(n_assets)]

    universe.bars = new_bars
    universe.assets = new_assets

    assert list(universe.bars) == new_bars
    assert list(universe.assets) == new_assets


@pytest.mark.parametrize('n_bars', params_n_bars[:1])
@pytest.mark.parametrize('n_assets', params_n_assets[:1])
def test_set(n_bars, n_assets):
    """
    Tests setting bars, assets when initializing.
    """
    bars = [f'MyBar{i}' for i in range(n_bars)]
    assets = [f'MyAsset{i}' for i in range(n_assets)]
    prices = make_randomuniverse(n_bars, n_assets).prices

    universe = Universe(prices, bars=bars, assets=assets)

    assert (universe.bars == bars).all()
    assert (universe.assets == assets).all()


@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_error_nan(n_bars, n_assets):
    """
    Test that Universe rejects np.nan.
    """
    prices = make_randomuniverse(n_bars, n_assets).prices
    prices.iat[n_bars // 2, n_assets // 2] = np.nan
    with pytest.raises(ValueError):
        universe = Universe(prices)
        print(universe)


@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_error_inf(n_bars, n_assets):
    """
    Test that Universe rejects np.inf.
    """
    prices = make_randomuniverse(n_bars, n_assets).prices
    prices.iat[n_bars // 2, n_assets // 2] = np.inf
    with pytest.raises(ValueError):
        universe = Universe(prices)
        print(universe)


# @pytest.mark.parametrize('n_bars', params_n_bars[:1])
# @pytest.mark.parametrize('n_assets', params_n_assets[:1])
# def test_error_NA(n_bars, n_assets):
#     prices = make_randomuniverse(n_bars, n_assets).prices
#     prices.iat[n_bars // 2, n_assets // 2] = pd.NA
#     with pytest.raises(ValueError):
#         universe = Universe(prices)


@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_error_nonunique_bar(n_bars, n_assets):
    bars = [f'MyBar{i}' for i in range(n_bars)]
    bars[n_bars // 2] = 'MyBar0'

    prices = make_randomuniverse(n_bars, n_assets).prices
    prices.index = bars

    with pytest.raises(ValueError):
        universe = Universe(prices)
        print(universe)


@pytest.mark.parametrize('n_bars', params_n_bars[-1:])
@pytest.mark.parametrize('n_assets', params_n_assets[-1:])
def test_error_nonunique_assets(n_bars, n_assets):
    assets = [f'MyAsset{i}' for i in range(n_assets)]
    assets[n_assets // 2] = 'MyAsset0'
    print(assets)

    prices = make_randomuniverse(n_bars, n_assets).prices
    prices.columns = assets

    with pytest.raises(ValueError):
        universe = Universe(prices)
        print(universe)
