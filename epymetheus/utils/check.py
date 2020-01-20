import numpy as np


def check_prices(prices):
    if np.isnan(prices).all(None):
        raise ValueError('Price has NA')
    if np.isinf(prices).all(None):
        raise ValueError('Price has INF')
