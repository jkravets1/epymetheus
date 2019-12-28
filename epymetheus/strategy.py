from abc import ABCMeta, abstractmethod

class TradeStrategy(metaclass=ABCMeta):
    """
    Represents a strategy to trade.

    Paramters
    ---------
    - name : str, optional
        The name.
    - description : str, optional
        The detailed description.

    Abstract method
    ---------------
    - logic : function (Universe -> list of trade)
        Algorithm that receives ``Universe`` and returns
        an iterable of ``trade``.

    Examples
    --------

    >>> class MyTradeStrategy(epymetheus.TradeStrategy):
    >>>     '''This is my favorite strategy.'''
    >>>
    >>>     def logic(universe, my_parameter):
    >>>         ...
    >>>         yield epymetheus.Trade(...)
    >>>
    >>> my_strategy = MyTradeStrategy(my_parameter=0.01)
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

    @property
    def parameters(self):
        """Parameters of strategy as ``dict``."""
        return self._parameters

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
