# import pytest  # noqa

# import random
# import numpy as np

# from epymetheus import TradeStrategy
# from epymetheus import History
# from epymetheus.datasets import make_randomwalk
# from epymetheus.benchmarks import RandomTrader

# params_seed = [42]
# params_n_bars = [100, 1000]
# params_n_assets = [10, 100]
# params_n_trades = [10, 100]


# class MockStrategy(TradeStrategy):
#     def logic(self, universe):
#         pass


# def make_strategy(universe=None, trades=None):
#     """
#     Return strategy with attributes universe and trades.

#     Returns
#     -------
#     strategy : TradeStrategy
#     """
#     strategy = MockStrategy()
#     if universe:
#         strategy.universe = universe
#     if trades:
#         strategy.trades = trades
#     return strategy


# def make_random_trades(universe, n_trades, seed):
#     random_trader = RandomTrader(n_trades=n_trades, seed=seed)
#     trades = random_trader.run(universe).trades
#     return list(trades)  # for of array is slow


# # --------------------------------------------------------------------------------


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_bars', params_n_bars)
# @pytest.mark.parametrize('n_assets', params_n_assets)
# @pytest.mark.parametrize('n_trades', params_n_trades)
# def test_trade_id(seed, n_bars, n_assets, n_trades):
#     """
#     Test trade_id and order_id.
#     """
#     universe = make_randomwalk(n_bars, n_assets)
#     trades = make_random_trades(universe, n_trades, seed)

#     expected = []
#     for i, trade in enumerate(trades):
#         expected += [i for _ in range(len(trade.asset))]

#     strategy = make_strategy(universe=universe, trades=trades)
#     _get_trade_index = History()._get_trade_index

#     assert np.equal(_get_trade_index(strategy), expected).all()


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_bars', params_n_bars)
# @pytest.mark.parametrize('n_assets', params_n_assets)
# @pytest.mark.parametrize('n_trades', params_n_trades)
# def test_order_id(seed, n_bars, n_assets, n_trades):
#     """
#     Test trade_id and order_id.
#     """
#     universe = make_randomwalk(n_bars, n_assets)
#     trades = make_random_trades(universe, n_trades, seed)

#     expected = []
#     for i, trade in enumerate(trades):
#         expected += [i for _ in range(len(trade.asset))]
#     expected = list(range(len(expected)))

#     strategy = make_strategy(universe=universe, trades=trades)
#     _get_order_index = History()._get_order_index

#     assert np.equal(_get_order_index(strategy), expected).all()


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_bars', params_n_bars)
# @pytest.mark.parametrize('n_assets', params_n_assets)
# @pytest.mark.parametrize('n_trades', params_n_trades)
# def test_asset_id(seed, n_bars, n_assets, n_trades):
#     np.random.seed(seed)
#     random.seed(seed)

#     universe = make_randomwalk(n_bars, n_assets)
#     trades = make_random_trades(universe, n_trades, seed)

#     expected = []
#     for i, trade in enumerate(trades):
#         # Asset name is 'Asset{i}'
#         expected += [int(a[5:]) for a in trade.asset]

#     strategy = make_strategy(universe=universe, trades=trades)
#     _get_asset_id = History()._get_asset_id

#     assert np.equal(_get_asset_id(strategy), expected).all()


# @pytest.mark.parametrize('seed', params_seed)
# @pytest.mark.parametrize('n_bars', params_n_bars)
# @pytest.mark.parametrize('n_assets', params_n_assets)
# @pytest.mark.parametrize('n_trades', params_n_trades)
# def test_lot(seed, n_bars, n_assets, n_trades):
#     np.random.seed(seed)
#     random.seed(seed)

#     universe = make_randomwalk(n_bars, n_assets)
#     trades = make_random_trades(universe, n_trades, seed)

#     expected = []
#     for i, trade in enumerate(trades):
#         expected += [lot for lot in trade.lot]  # Asset name is 'Asset{i}'

#     strategy = make_strategy(universe=universe, trades=trades)
#     _get_lot = History()._get_lot

#     assert np.equal(_get_lot(strategy), expected).all()
