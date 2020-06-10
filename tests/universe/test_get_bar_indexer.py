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
def test_get_bar_indexer(universe):
    i = universe.get_bar_indexer("Bar0")
    i_expected = [0]
    assert np.array_equal(i, i_expected)

    i = universe.get_bar_indexer(["Bar2", "Bar1"])
    i_expected = [2, 1]
    assert np.array_equal(i, i_expected)

    i = universe.get_bar_indexer(["BarNA", "Bar1"])
    i_expected = [-1, 1]
    assert np.array_equal(i, i_expected)


@pytest.mark.parametrize("universe", params_universe)
def test_get_asset_indexer(universe):
    i = universe.get_asset_indexer("Asset0")
    i_expected = [0]
    assert np.array_equal(i, i_expected)

    i = universe.get_asset_indexer(["Asset2", "Asset1"])
    i_expected = [2, 1]
    assert np.array_equal(i, i_expected)

    i = universe.get_asset_indexer(["AssetNA", "Asset1"])
    i_expected = [-1, 1]
    assert np.array_equal(i, i_expected)
