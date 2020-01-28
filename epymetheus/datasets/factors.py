# import numpy as np

# from .. import Universe
# import pandas as pd


# def make_factormodeled(
#     n_bars=3000,
#     n_assets=10,
#     n_factors=3,
#     assets=None,
#     bars=None,
#     date_bar=True,
#     begin_date='2000-01-01',
#     amp_factors=0.01,
#     amp_alpha=0.01,
#     seed=None,
# ):
#     if seed:
#         np.random.seed(seed)
#     # susceptibility to factors
#     b = np.random.randn(n_factors, n_assets)

#     factor_returns = amp_factors * np.random.randn(n_bars, n_factors)
#     alphas = amp_alpha * np.random.randn(n_bars)

#     factor_returns[0, :] = 0.0
#     alphas[0] = 0.0

#     syst_returns = np.dot(factor_returns, b)
#     nonsyst_returns = np.broadcast_to(alphas, (n_assets, n_bars)).T
#     returns = syst_returns + nonsyst_returns

#     prices = 100 * (1 + returns).cumprod(axis=0)
#     data = pd.DataFrame(prices)

#     universe = Universe(data=data, name='Factor Modeled')
#     if assets is not None:
#         universe.assets = assets
#     if bars is not None:
#         universe.bars = bars

#     return universe
