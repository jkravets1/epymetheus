from epymetheus import AllocationStrategy


class Universal(AllocationStrategy):
    """
    Allocate the wealth with the weight proportional to
    the cumulative return of each asset.

    Parameters
    ----------
    - name : str, default 'Universal Portfolio'
        The name of the strategy.
    - description : str, default 'Bets on the best stock with hindsight.'
        The description of the strategy.
    """
    def logic(universe):
        cum_return = universe / universe.iloc[0, :]
        df = cum_return.div(cum_return.sum(axis=1), axis=0) / universe
        return df
