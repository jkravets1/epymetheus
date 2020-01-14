from abc import ABCMeta, abstractmethod
from inspect import cleandoc
from time import time

from .history import History
from .transaction import Transaction
from .wealth import Wealth


class NotRunnedError(Exception):
    pass

class TradeStrategy(metaclass=ABCMeta):
    """
    Represents a strategy to trade.

    Parameters
    ----------
    - name : str, optional
        Name of the strategy.
    - description : str, optional
        Description of the strategy.
        If None, docstring.

    Attributes
    ----------
    - universe
    - history
    - transaction
    - wealth

    Examples
    --------
    Define strategy by subclassing:
    >>> class MyTradeStrategy(TradeStrategy):
    >>>     '''This is my favorite strategy.'''
    >>>
    >>>     def logic(universe, my_parameter):
    >>>         ...
    >>>         yield epymetheus.Trade(...)

    Initialize:
    >>> my_strategy = MyTradeStrategy(my_parameter=0.1)
    >>> my_strategy.name
    'MyTradeStrategy'
    >>> my_strategy.description
    'This is my favorite strategy.'
    >>> my_strategy.params
    {'my_parameter': 0.1}

    Set context (optional):
    >>> spx = ...  # Fetch S&P 500 historical prices
    >>> my_strategy.context(
    ...     slippage=0.001,
    ...     benchmark=spx,
    ... )

    Run:
    >>> universe = Universe(...)
    >>> my_strategy.run(universe)
    """
    def __init__(self, **kwargs):
        self.params = kwargs
        self.is_runned = False

    @property
    def name(self):
        """Name of the strategy."""
        return self.__class__.__name__

    @property
    def description(self):
        """Detailed description of the strategy."""
        return cleandoc(self.__class__.__doc__)

    @abstractmethod
    def logic(self, universe, **kwargs):
        """
        Logic to return iterable of ``Trade`` from ``Universe``.

        Parameters
        ----------
        - universe : Universe
            Universe to apply the logic.
        - kwargs
            Parameters of the trade strategy.
        """
        raise NotImplementedError(
            'Logic must be implemented in a subclass.'
        )

    def context(self,
                metrics=['fin_wealth']):
        pass  # TODO

    def run(self, universe, verbose=True):
        self.universe = universe

        if verbose:
            begin_time = time()
            print('Evaluating wealth ...')

        self.history = History._from_strategy(self)
        self.transaction = Transaction._from_strategy(self)
        self.wealth = Wealth._from_strategy(self)

        if verbose:
            print('Done.')
            print(f'Runtime : {time() - begin_time:.1f}sec')

        self.is_runned = True

        return self
