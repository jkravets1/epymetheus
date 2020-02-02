from time import time

from .utils import Bunch


class Wealth(Bunch):
    """
    Represent time-series of wealth.

    Attributes
    ----------
    - wealth
    """
    def __init__(self, strategy=None, verbose=True, **kwargs):
        if strategy is not None:
            super().__init__(**self.__from_strategy(strategy, verbose=verbose))
        else:
            super().__init__(**kwargs)

    @classmethod
    def __from_strategy(cls, strategy, verbose=True):
        """
        Initialize wealth from strategy.

        Parameters
        ----------
        - strategy : TradeStrategy
        - verbose : bool
        """
        if verbose:
            begin_time = time()
            print('Evaluating wealth ... ', end='')

        wealth = cls()
        wealth.bars = bars=strategy.universe.bars
        wealth.wealth = wealth=strategy.wealth_

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return wealth
