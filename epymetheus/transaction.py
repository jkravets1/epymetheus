from time import time

from .utils import Bunch


class Transaction(Bunch):
    """
    Represent transaction history.

    Attributes
    - (name of assets) : array, (n_bars, )
        Transaction of each asset.
    """
    def __init__(self, strategy=None, verbose=True, **kwargs):
        if strategy is not None:
            super().__init__(**self.__from_strategy(strategy, verbose=verbose))
        else:
            super().__init__(**kwargs)

    @classmethod
    def __from_strategy(cls, strategy, verbose=True):
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
        begin_time = time()

        if verbose:
            print('Evaluating history ... ', end='')

        transaction = cls()
        transaction.bars = strategy.universe.bars
        transaction_matrix = strategy._transaction_matrix

        for asset_id, asset in enumerate(strategy.universe.assets):
            setattr(transaction, asset, transaction_matrix[:, asset_id])

        if verbose:
            print(f'Done. (Runtime : {time() - begin_time:.2f} sec)')

        return transaction
