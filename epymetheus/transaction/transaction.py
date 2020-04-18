# from epymetheus.utils import TradeResult


# class Transaction(TradeResult):
#     """
#     Represent transaction history.

#     Attributes
#     ----------
#     - (name of assets) : array, (n_bars, )
#         Transaction of each asset.
#     """
#     @classmethod
#     def from_strategy(cls, strategy):
#         """
#         Initialize self from strategy.

#         Parameters
#         ----------
#         - strategy : TradeStrategy

#         Returns
#         -------
#         transaction : Transaction
#         """


# def transaction_matrix(strategy):
#     """
#     Return array representing transaction at each bar and asset.

#     Returns
#     -------
#     transaction_matrix : array, shape (n_bars, n_assets)

#     Examples
#     --------
#     >>> strategy.trades = [
#     ...     Trade(
#     ...         open_bar='01-01', close_bar='01-03',
#     ...         asset=['Asset0', 'Asset1'], lot=[1, -2], ...
#     ...     ),
#     ...     Trade(
#     ...         open_bar='01-02', close_bar='01-05',
#     ...         asset='Asset2', lot=3, ...
#     ...     ),
#     ... ]
#     >>> strategy._transaction_matrix
#     #       Asset0  Asset1  Asset2
#     array([[     1      -2       0]    # 01-01
#            [     0       0       3]    # 01-02
#            [    -1       2       0]    # 01-03
#            [     0       0       0]    # 01-04
#            [     0       0      -3]])  # 01-05
#     """
#     # (n_bars, n_orders) . (n_orders, n_orders) . (n_orders, n_assets)
#     return multi_dot([
#         strategy.universe._bar_onehot(strategy.open_bar_ids).T
#         - strategy.universe._bar_onehot(strategy.close_bar_ids).T,
#         np.diag(strategy.lot),
#         strategy.universe._asset_onehot(strategy.asset_id),
#     ])
