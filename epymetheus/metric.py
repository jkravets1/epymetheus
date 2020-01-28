# import numpy as np


# def final_wealth(wealth):
#     return wealth[-1]


# def return_total(wealth):
#     return wealth[-1] / wealth[0] - 1


# def return_perbar(wealth, compound=False):
#     if compound:
#         pass
#     else:
#         return_total(wealth) / wealth.n_bars


# def vola_perbar(wealth):
#     """Returns volatility per a bar."""
#     return wealth.pct_change().std() / np.sqrt(wealth.n_bars)


# def sharpe_ratio(wealth):
#     """Returns Sharpe ratio."""
#     return return_perbar(wealth) / vola_perbar(wealth)


# def max_drop(wealth):
#     return np.min(wealth - wealth.cummax())


# def max_drawdown(wealth):
#     return np.min(1 - wealth / wealth.cummax())


# def sortino_ratio(wealth):
#     pass


# def benchmark_correlation(wealth, benchmark):
#     return np.corrcoef(wealth, benchmark)[0, 1]
