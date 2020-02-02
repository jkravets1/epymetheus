import pytest

import numpy as np

from epymetheus.datasets import fetch_usstock


# --------------------------------------------------------------------------------


def test_utstock():
    universe = fetch_usstock()
    assert not np.isnan(universe.prices.values).any(axis=None)
