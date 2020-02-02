from abc import ABCMeta, abstractmethod
from inspect import cleandoc
from time import time

import pandas as pd

from .history import History
from .transaction import Transaction
from .wealth import Wealth


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
    >>> my_strategy.setup(
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

    # def setup(self,
    #           metrics=['fin_wealth'],
    #           slippage=0.0,
    #           benchmark=None,
    #           ):
    #     """
    #     Configure the context of backtesting.

    #     Parameters
    #     ----------
    #     - metrics
    #     - slippage
    #     - benchmark
    #     """
    #     self.context = Bunch(
    #         metrics=metrics,
    #         slippage=slippage,
    #         benchmark=benchmark,
    #     )

    @property
    def n_trades(self):
        return len(self.trades)

    @property
    def n_orders(self):
        return sum(trade.n_orders for trade in self.trades)

    def run(self, universe, verbose=True, save={}):
        """
        Run a backtesting of strategy.
        Set attributes `history`, `transaction` and `wealth`.

        Parameters
        ----------
        - universe : Universe
        - verbose : bool
        - save : dict
        """
        begin_time = time()

        if verbose:
            print('Running ... ')

        self.universe = universe
        self.trades = self._get_trades(verbose=verbose)
        self.history = History(strategy=self, verbose=verbose)
        self.transaction = Transaction(strategy=self, verbose=verbose)
        self.wealth = Wealth(strategy=self, verbose=verbose)

        if verbose:
            print('Done.')
            runtime = time() - begin_time
            print(f'Runtime : {runtime:.1f}sec')

        self.is_runned = True

        # save result TODO: check valid input
        if save:
            for attr, path in save.items():
                data = pd.DataFrame(getattr(self, attr))
                data.to_csv(path)

        return self

    def _get_trades(self, verbose):
        """
        Parameters
        ----------
        - self
            TradeStrategy; necessary attributes:
            * universe
        - verbose : bool

        Returns
        -------
        - list of Trade
        """
        if verbose:
            def generate_trades():
                trades = self.logic(self.universe, **self.params)
                if not trades:
                    return []
                for i, trade in enumerate(trades):
                    print(f'\rGenerating {i + 1} trades ... ', end='')
                    yield trade
                print('Done.')
            return list(generate_trades())
        else:
            return list(self.logic(self.universe, **self.params))
