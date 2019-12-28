import numpy as np


def min_std(r, c):
    e = np.ones(len(r))
    cinv = np.linalg.inv(c)

    Aee = e.dot(cinv.dot(e))
    Aer = e.dot(cinv.dot(r))
    Arr = r.dot(cinv.dot(r))
    B = Aee * Arr - Aer ** 2

    def min_std(r):
        v = (Aee * (r ** 2) - 2 * Aer * r + Arr) / B
        return np.sqrt(v)

    return min_std
