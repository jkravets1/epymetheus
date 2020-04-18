from time import time

from epymetheus.utils import TradeResult


class Wealth(TradeResult):
    """
    Represent time-series of wealth.

    Attributes
    ----------
    - wealth : numpy.array, shape (n_bars, )
    - bars : numpy.array, shape (n_bars, )
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
            msg = 'Evaluating wealth'
            print(f'{msg:<22} ... ', end='')
            begin_time = time()

        wealth = cls(
            bar=cls._get_bars(strategy),
            wealth=cls._get_wealth(strategy),
        )

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return wealth

    @staticmethod
    def _get_bars(strategy):
        return strategy.universe.bars

    @staticmethod
    def _get_wealth(strategy):
        return reduce(np.add, (
            trade.array_pnl() for trade in strategy.trades
        ))

    def to_series(self, name='wealth', copy=False):
        """
        Represent self as `pandas.Series`.

        Parameters
        ----------
        - name : str, default 'wealth'
            The name to give to the Series.
        - copy : bool, default False
            Copy input data.

        Returns
        -------
        series_wealth : pandas.Series
        """
        return pd.Series(self.wealth, index=self.bars, name=name, copy=copy)

    def to_dataframe(self):
        """
        Represent self as `pandas.DataFrame`.

        Parameters
        ----------
        - copy : bool, default False
            Copy input data.

        Returns
        -------
        df_wealth : pandas.DataFrame
        """
        return pd.DataFrame(self).set_index('bars')
