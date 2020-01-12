from abc import ABCMeta, abstractmethod
from inspect import cleandoc

class TradeStrategy(metaclass=ABCMeta):
    """
    Represents a strategy to trade.

    Paramters
    ---------
    - name : str, optional
        Name of the strategy.
    - description : str, optional
        Description of the strategy.
        If None, docstring.

    Examples
    --------
    Defining:
    >>> class MyTradeStrategy(TradeStrategy):
    >>>     '''This is my favorite strategy.'''
    >>>
    >>>     def logic(universe, my_parameter):
    >>>         ...
    >>>         yield epymetheus.Trade(...)

    Initializing:
    >>> my_strategy = MyTradeStrategy(my_parameter=0.01)
    >>> my_strategy.name
    'MyTradeStrategy'
    >>> my_strategy.description
    'This is my favorite strategy.'

    Running:
    >>> universe = Universe(...)
    >>> backtester = Backtester(...)
    >>> backtester.run(strategy, universe)
    """
    def __init__(self, **kwargs):
        self.params = kwargs

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
        pass
