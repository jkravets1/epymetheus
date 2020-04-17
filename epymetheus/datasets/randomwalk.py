import numpy as np
import pandas as pd

from epymetheus import Universe


def make_randomwalk(
    n_bars=1000,
    n_assets=10,
    volatility=0.01,
    name='RandomWalk',
    bars=None,
    assets=None,
    seed=None,
):
    """
    Return Universe whose prices are random-walks.
    Daily returns follow log-normal distribution.

    Parameters
    ----------
    - n_bars : int, default 1000
    - n_assets : int, default 10
    - volatility : float, default 0.01
    - name : str, default='RandomWalk'
    - bars
    - assets
    - seed : int

    Returns
    -------
    Universe
    """
    data = np.random.lognormal(
        sigma=volatility, size=(n_bars, n_assets)
    ).cumprod(axis=0)
    data /= data[0, :]

    bars = bars or list(range(n_bars))
    assets = assets or [str(i) for i in range(n_assets)]

    prices = pd.DataFrame(data, index=bars, columns=assets)

    return Universe(prices, name=name)
