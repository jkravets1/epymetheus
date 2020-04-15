from abc import ABCMeta, abstractmethod
from inspect import cleandoc
from time import time

import numpy as np

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

    def run(self, universe, verbose=True, save={}):
        """
        Run a backtesting of strategy.
        Set attributes `history`, `transaction` and `wealth`.

        Parameters
        ----------
        - universe : Universe
        - verbose : bool
        - save : dict

        Returns
        -------
        self
        """
        self.verbose = verbose

        if verbose:
            begin_time = time()
            print('Running ... ')

        self.universe = universe
        self.trades = self.__generate_trades(verbose=verbose)
        self.__is_run = True

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return self

    def __generate_trades(self, verbose=True):
        """
        Parameters
        ----------
        - verbose : bool

        Returns
        -------
        - list of Trade
        """
        def iter_trades(verbose):
            if verbose:
                begin_time = time()
                for i, trade in enumerate(self.logic(self.universe) or []):
                    msg = f'Generating {i + 1} trades'
                    print(f'\r{msg:<22} ({trade.open_bar}) ...', end='')
                    yield trade
                print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')
            else:
                for trade in self.logic(self.universe) or []:
                    yield trade

        trades = list(iter_trades(verbose))

        if len(trades) == 0:
            raise RuntimeError('No trades')

        return trades

    @property
    def name(self):
        """Return name of the strategy."""
        return self.__class__.__name__

    @property
    def description(self):
        """Return detailed description of the strategy."""
        return cleandoc(self.__class__.__doc__)

    @property
    def is_run(self):
        return getattr(self, '__is_run', False)

    @property
    def n_trades(self):
        return len(self.trades)

    @property
    def n_orders(self):
        return sum(trade.n_orders for trade in self.trades)

    @property
    def n_bars(self):
        return self.universe.n_bars

    @property
    def n_assets(self):
        return self.universe.n_assets

    @property
    def history(self):
        return History(strategy=self)

    @property
    def transaction(self):
        return Transaction(strategy=self)

    @property
    def wealth(self):
        return Wealth(strategy=self)

    @property
    def asset_id(self):
        """
        Return asset id of each order.

        Returns
        -------
        asset_id : array, shape (n_orders, )

        Examples
        --------
        >>> strategy.universe.assets
        >>> Index(['Asset0', 'Asset1', 'Asset2', ...])
        >>> strategy.trades = [
        ...     Trade(asset=['Asset0', 'Asset1'], ...),
        ...     Trade(asset=['Asset2'], ...),
        ... ]
        >>> strategy.assets
        array([ 0, 1, 2])
        """
        return self.universe.assets.get_indexer(
            np.concatenate([
                trade.asset for trade in self.trades
            ])
        )

    @property
    def lot(self):
        """
        Return lot of each order.

        Returns
        -------
        lot : array, shape (n_orders, )

        Examples
        --------
        >>> strategy.trades = [
        ...     Trade(lot=[1, -2], ...),
        ...     Trade(lot=[3], ...),
        ... ]
        >>> strategy.lots
        array([  1, -2,  3])
        """
        return np.concatenate([trade.lot for trade in self.trades])

    @property
    def open_bar_ids(self):
        return pipe.open_bar_ids(self, columns='orders')

    @property
    def open_bars(self):
        return self.universe.bars[self.open_bar_ids]

    @property
    def shut_bar_ids(self):
        return pipe.shut_bar_ids(self, columns='orders')

    @property
    def shut_bars(self):
        return self.universe.bars[self.shut_bar_ids]

    @property
    def close_bar_ids(self):
        return pipe._close_bar_ids_from_signals(self, columns='orders')

    @property
    def close_bars(self):
        return self.universe.bars[self.close_bar_ids]

    @property
    def takes(self):
        return pipe.takes(self, columns='orders')

    @property
    def stops(self):
        return pipe.stops(self, columns='orders')

    @property
    def durations(self):
        return pipe.durations(self)

    @property
    def open_prices(self):
        return pipe.open_prices(self)

    @property
    def close_prices(self):
        return pipe.close_prices(self)

    @property
    def gains(self):
        return pipe.gains(self)

    @property
    def wealth_(self):
        return pipe.wealth(self)

    @property
    def transaction_matrix(self):
        return pipe.transaction_matrix(self)

    @property
    def net_exposure(self):
        return pipe.net_exposure(self)

    @property
    def abs_exposure(self):
        return pipe.abs_exposure(self)
