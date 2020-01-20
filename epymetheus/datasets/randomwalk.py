import numpy as np
import pandas as pd

from epymetheus import Universe


def make_randomwalk(
    n_bars=1000,
    n_assets=100,
    volatility=0.001,
    distribution='normal',
    name='RandomWalker',
):
    """
    Return Universe of which prices are random-walks.

    Parameters
    ----------
    - n_bars : int, default=1000
    - n_assets : int, default=100
    - volatility : float, default=0.01
    - distribution : {'normal'}, default='normal'
    - name : str, default='RandomWalker'
    """
    assets = [str(i) for i in range(n_assets)]

    if distribution == 'normal':
        random = np.random.randn(n_bars, n_assets)
    prices = pd.DataFrame(
        np.cumprod(1.0 + volatility * random, axis=0), columns=assets
    )

    return Universe(prices, name=name)
