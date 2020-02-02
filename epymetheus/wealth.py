from time import time

from .utils import TradeResult


class Wealth(TradeResult):
    """
    Represent time-series of wealth.

    Attributes
    ----------
    - wealth
    """
    @classmethod
    def from_strategy(cls, strategy, verbose=True):
        """
        Initialize wealth from strategy.

        Parameters
        ----------
        - strategy : TradeStrategy
        - verbose : bool
        """
        if verbose:
            print('Evaluating wealth ... ', end='')
            begin_time = time()

        wealth = cls()
        wealth.bars = strategy.universe.bars
        wealth.wealth = strategy.wealth_

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return wealth
