from abc import ABCMeta, abstractmethod
from inspect import cleandoc
from time import time

import numpy as np

from epymetheus.exceptions import NoTradeError
from epymetheus.history import History
from epymetheus.transaction import Transaction
from epymetheus.wealth import Wealth
from epymetheus import pipe


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
    - params : dict
        Parameters of the logic.

    Attributes
    ----------
    - trades : array of Trade, shape (n_trades, )
    - n_trades : int
    - n_orders : int
    - universe : Universe
    - history : History
    - transaction : Transaction
    - wealth : Wealth

    Examples
    --------
    Define strategy by subclassing:
    >>> class MyTradeStrategy(TradeStrategy):
    ...     '''
    ...     This is my favorite strategy.
    ...     '''
    ...     def __init__(self, my_parameter):
    ...         self.my_parameter = my_parameter
    ...
    ...     def logic(self, universe):
    ...         ...
    ...         yield Trade(...)

    Initialize:
    >>> my_strategy = MyTradeStrategy(my_parameter=0.1)
    >>> my_strategy.name
    'MyTradeStrategy'
    >>> my_strategy.description
    'This is my favorite strategy.'
    >>> my_strategy.params
    {'my_parameter': 0.1}

    Run:
    >>> universe = Universe(...)
    >>> my_strategy.run(universe)

    Todo
    ----
    - dump trades in a light data structure
    """
    def __init__(self):
        """Initialize self."""

    @abstractmethod
    def logic(self, universe):
        """
        Logic to generate `Trade` from `Universe`.

        Parameters
        ----------
        - universe : Universe
            Universe to apply the logic.

        Yields
        ------
        trade : Trade
        """

    def run(self, universe, verbose=True):
        """
        Run a backtesting of strategy.

        Parameters
        ----------
        - universe : Universe
            Universe with which self is run.
        - verbose : bool, default True
            Vermose mode.

        Returns
        -------
        self
        """
        if verbose:
            begin_time = time()
            print('Running ... ')

        self.universe = universe
        self.__generate_trades(universe=universe, verbose=verbose)
        self.__execute_trades(universe=universe, verbose=verbose)

        self._is_run = True

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return self

    def __generate_trades(self, universe, verbose=True):
        """
        Generate trades according to `self.logic`.
        It sets `self.trades`.

        Parameters
        ----------
        - verbose : bool

        Returns
        -------
        self : TradeStrategy
        """
        def iter_trades(verbose):
            if verbose:
                begin_time = time()
                for i, trade in enumerate(self.logic(universe) or []):
                    print(f'\rGenerating {i + 1} trades ({trade.open_bar}) ... ', end='')
                    yield trade
                print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')
            else:
                for trade in self.logic(universe) or []:
                    yield trade

        self.trades = list(iter_trades(verbose))

        if len(self.trades) == 0:
            raise NoTradeError('No trades')

        return self

    def __execute_trades(self, universe, verbose=True):
        """
        Execute trades.

        Returns
        -------
        self : TradeStrategy
        """
        if verbose:
            begin_time = time()
            for i, trade in enumerate(self.trades):
                print(f'\rExecuting {i + 1} trades ... ', end='')
                trade.execute(universe)
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')
        else:
            for trade in self.trades:
                trade.execute(universe)

        return self

    @property
    def name(self):
        """Return name of the strategy."""
        return self.__class__.__name__

    @property
    def description(self):
        """Return detailed description of the strategy."""
        return cleandoc(self.__class__.__doc__)

    @property
    def params(self):
        """
        Return parameters of self as `dict`.

        Returns
        -------
        parameters : dict
            Names and values of parameters.

        Examples
        --------
        >>> class MyStrategy:
        ...     def __init__(self, param1, param2):
        ...         self.param1 = param1
        ...         self.param2 = param2
        ...
        >>> my_strategy = MyStrategy(param1=1.2, param2=3.4)
        >>> my_strategy.params
        {'param1': 1.2, 'param2': 3.4}
        """
        return self.__dict__

    @property
    def is_run(self):
        return getattr(self, '_is_run', False)

    @property
    def n_trades(self):
        return len(self.trades)

    @property
    def n_orders(self):
        return sum(trade.n_orders for trade in self.trades)

    @property
    def history(self):
        return History(strategy=self)

    @property
    def transaction(self):
        return Transaction(strategy=self)

    @property
    def wealth(self):
        return Wealth(strategy=self)
