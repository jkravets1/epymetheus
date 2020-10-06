from abc import abstractmethod

from .bunch import Bunch


class TradeResult(Bunch):
    """
    Bunch that can be initialized from Strategy.

    Abstractmethod
    --------------
    - from_strategy
        Initialize TradeResult from strategy.
    """

    def __init__(self, strategy=None, **kwargs):
        if strategy is not None:
            super().__init__(**self.from_strategy(strategy))
        else:
            super().__init__(**kwargs)

    @classmethod
    @abstractmethod
    def from_strategy(cls, strategy, verbose):
        """
        Initialize TradeResult from strategy.

        Parameters
        ----------
        - strategy : Strategy
        - verbose : bool

        Returns
        -------
        traderesult : TradeResult
        """
