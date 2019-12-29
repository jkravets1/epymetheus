from .trade import TradeHistory, Transaction, Wealth
from time import time

class Backtester:
    """
    Parameters
    ----------
    - benchmark : pandas.Series

    Attributes
    ----------
    - strategy_
    - universe_
    - history_
    - transaction_
    - position_

    Examples
    --------
    >>> backtester = BackTester()
    >>> backtest.run()
    """
    def __init__(self, benchmark=None):
        self.benchmark = benchmark

    def run(self, strategy, universe, verbose=False):
        begin_time = time()

        self.strategy_ = strategy
        self.universe_ = universe

        if verbose:
            print('Generating trades ...')
        trades = list(strategy.logic(universe, **strategy.params))

        if verbose:
            print('Evaluating wealth ...')
        self.history_ = TradeHistory.from_trades(trades, universe)
        self.transaction_ = Transaction.from_trades(trades, universe)
        self.wealth_ = Wealth.from_transaction(self.transaction_, universe)
        self.runtime_ = time() - begin_time

        if verbose:
            print('Done.')
            print(f'Runtime : {self.runtime_:.1f}sec')
        return self
