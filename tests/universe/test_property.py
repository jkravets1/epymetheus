import pytest

import numpy as np
import pandas as pd

from epymetheus import Universe


universe = Universe(
    prices=pd.DataFrame(
        {"Asset0": [0, 1, 2, 3], "Asset1": [0, 1, 2, 3], "Asset2": [0, 1, 2, 3],},
        index=["Bar0", "Bar1", "Bar2", "Bar3"],
    )
)

params_universe = [universe]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize("universe", params_universe)
def test_bars(universe):
    assert np.array_equal(universe.bars, ["Bar0", "Bar1", "Bar2", "Bar3"])


@pytest.mark.parametrize("universe", params_universe)
def test_assets(universe):
    assert np.array_equal(universe.assets, ["Asset0", "Asset1", "Asset2"])


@pytest.mark.parametrize("universe", params_universe)
def test_n_bars(universe):
    assert universe.n_bars == 4


@pytest.mark.parametrize("universe", params_universe)
def test_n_assets(universe):
    assert universe.n_assets == 3
