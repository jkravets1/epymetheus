import numpy as np


def check_prices(prices):
    if np.isnan(prices).any(None):
        raise ValueError('Price has NA')
    if np.isinf(prices).any(None):
        raise ValueError('Price has INF')
