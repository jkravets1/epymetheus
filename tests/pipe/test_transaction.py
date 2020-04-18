# import pytest  # noqa

# import numpy as np
# import pandas as pd

# from epymetheus import Universe, Trade, TradeStrategy
# from epymetheus.pipe.transaction import (
#     transaction_matrix,
# )


# # TODO this is just tentative; add multiple and robust tests


# def make_universe(n_bars, n_assets, pricedata=None):
#     if pricedata is None:
#         pricedata = np.zeros((n_bars, n_assets))
#     prices = pd.DataFrame(
#         pricedata,
#         index=[f'Bar{i}' for i in range(n_bars)],
#         columns=[f'Asset{i}' for i in range(n_assets)],
#     )
#     return Universe(prices)


# class MockStrategy(TradeStrategy):
#     def logic(self, universe):
#         pass


# def make_strategy(universe=None, trades=None):
#     strategy = MockStrategy()
#     if universe:
#         strategy.universe = universe
#     if trades:
#         strategy.trades = trades
#     return strategy


# # --------------------------------------------------------------------------------


# def test_transaction():
#     universe = make_universe(5, 3)
#     trades = [
#         Trade(asset=['Asset0', 'Asset1'], lot=[1, -2], open_bar='Bar0', shut_bar='Bar2'),
#         Trade(asset='Asset2', lot=3, open_bar='Bar1', shut_bar='Bar4'),
#     ]
#     strategy = make_strategy(universe=universe, trades=trades)

#     expected = np.array([
#         [1, -2, 0],
#         [0, 0, 3],
#         [-1, 2, 0],
#         [0, 0, 0],
#         [0, 0, -3],
#     ])

#     assert np.equal(transaction_matrix(strategy), expected).all()
