from abc import ABCMeta, abstractmethod
from inspect import cleandoc

import pandas as pd

from epymetheus.core.universe import Universe


class Allocation(pd.core.frame.DataFrame):
    """
    Represent online asset allocation.

    Inheriting ``pandas.DataFrame``.

    Attributes
    ----------
    - data : ndarray, Iterable, dict, DataFrame
        Array of historical position data.
        Each value represents "value of asset / total wealth".
    - index : index, array-like
        Period to allocate wealth.
    - columns : index, array-like
        List of assets.
    - begin_date : datetime.date
        Begin date of allocation.
    - end_date : datetime.date
        End date of allocation.
    - duration : datetime.timedelta
        The duration to allocate wealth.

    Examples
    --------

    The following ``Allocation`` means one allocates
    70 % of wealth to VTI, 50 % to VEA, and -10 % to VWO
    (which is a short position) from the beginning to the end of 2018.
    The ratio adds up to 1.1, which means reveraging.

    >>> allocation
                VTI  VEA   VWO
    2018-01-01  0.7  0.5  -0.1
    2018-01-02  0.7  0.5  -0.1
    ..........  ...  ...   ...
    2018-12-31  0.7  0.5  -0.1
    """
    def __init__(
        self,
        data=None,
        index=None,
        columns=None
    ):
        super(Allocation, self).__init__(
            data=data,
            index=index,
            columns=columns
        )
        self._begin_date = index[0]
        self._end_date = index[-1]
        self._duration = self.end_date - self.begin_date
        # TODO alias self.member, self.period

    @property
    def begin_date(self):
        return self.index[0]

    @property
    def end_date(self):
        return self.index[-1]

    @property
    def duration(self):
        return self.end_date - self.begin_date

    def pnl(
        self,
        universe: Universe
    ):
        """
        Return multiplicative profit and loss.

        Parameters
        ----------
        - universe: Universe
            Universe to evaluate the PnL with.

        Returns
        -------
        pandas.Series
        """
        return (self * universe.pct_change()).sum(axis=1)

    # def cumpnl(
    #     self,
    #     universe: Universe
    # ):
    #     """
    #     Evaluate cumulative profit-loss.

    #     Parameters
    #     ----------
    #     - universe: Universe
    #         Universe to evaluate the cumulative PnL with.
    #     """
    #     return (1 + self.pnl(universe)).cumprod()


class AllocationStrategy(metaclass=ABCMeta):
    """
    Represent asset allocation strategy.

    Attributes
    ----------
    - name : str, optional
        Name of.
    - description : str, optional
        The detailed description.

    Abstract Method
    ---------------
    - logic : function (Universe -> pandas.DataFrame)
        Algorithm that receives ``Universe`` and returns
        ``pandas.DataFrame`` of ``Allocation``.
    """
    def __init__(self, **kwargs):
        self._parameters = kwargs

    @property
    def name(self):
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
    def logic(
        self,
        universe: Universe,
        **kwargs
    ) -> pd.DataFrame:
        """
        Logic to return DataFrame representing
        ``Allocation`` from ``Universe``.

        Parameters
        ----------
        - universe : Universe
            Universe to apply the logic.
        - kwargs
            Parameters of the allocation strategy.
        """
        pass

    def run(
        self,
        universe=None,
        path=None,
        # initial_wealth: Union[int, float] = None,
        # commission_rate: float = .0,
    ):
        pass  # TODO


class AllocationResult():

    def __init__(
        self,
        strategy: AllocationStrategy,
        universe: Universe,
    ):
        pass  # TODO
