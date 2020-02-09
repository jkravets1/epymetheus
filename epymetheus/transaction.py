from time import time

from epymetheus.utils import TradeResult


class Transaction(TradeResult):
    """
    Represent transaction history.

    Attributes
    ----------
    - (name of assets) : array, (n_bars, )
        Transaction of each asset.
    """
    @classmethod
    def from_strategy(cls, strategy, verbose=True):
        """
        Initialize self from strategy.

        Parameters
        ----------
        - strategy : TradeStrategy
        - verbose : bool

        Returns
        -------
        transaction : Transaction
        """
        if verbose:
            msg = 'Evaluating transaction'
            print(f'{msg:<22} ... ', end='')
            begin_time = time()

        transaction = cls()
        transaction.bars = strategy.universe.bars
        transaction_matrix = strategy.transaction_matrix

        for asset_id, asset in enumerate(strategy.universe.assets):
            setattr(transaction, asset, transaction_matrix[:, asset_id])

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return transaction
