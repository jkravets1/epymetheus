# from time import time

# from .history import History
# from .transaction import Transaction
# from .wealth import Wealth


# class Backtester:
#     """
#     Parameters
#     ----------

#     Attributes
#     ----------
#     - strategy_
#     - universe_
#     - history_
#     - transaction_
#     - position_

#     Examples
#     --------
#     >>> backtester = BackTester()
#     >>> backtest.run()
#     """
#     def __init__(self):
#         pass
#         # TODO initial_wealth, slippage, benchmark, ...

#     def run(self, strategy, universe, verbose=False):
#         begin_time = time()

#         self.strategy = strategy
#         self.universe = universe

#         if verbose:
#             print('Evaluating wealth ...')

#         self.history_ = TradeHistory._from_backtester(self)
#         self.transaction_ = Transaction._from_backtester(self)
#         self.wealth_ = Wealth._from_backtester(self)
#         # self.wealth_ = Wealth.from_transaction(self.transaction_, universe)

#         self.runtime_ = time() - begin_time

#         if verbose:
#             print('Done.')
#             print(f'Runtime : {self.runtime_:.1f}sec')

#         return self
