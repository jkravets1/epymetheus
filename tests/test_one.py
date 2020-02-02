import pytest
from ._utils import make_randomuniverse, generate_trades

import random
import numpy as np

from epymetheus import Trade, TradeStrategy


params_seed = [42, 1, 2, 3]
params_n_bars = [10, 1000]
params_n_assets = [1, 3, 100]
params_lot = [0.0, 1, 1.23, -1.23, 123.4, -123.4]
params_verbose = [True, False]


class OneTradeStrategy(TradeStrategy):
    """
    Yield a single trade.
    """
    def logic(self, universe, asset, lot, open_bar, close_bar):
        yield Trade(
            asset=asset,
            lot=lot,
            open_bar=open_bar,
            close_bar=close_bar,
        )


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('lot', params_lot)
@pytest.mark.parametrize('verbose', params_verbose)
def test_one(seed, n_bars, n_assets, lot, verbose):
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomuniverse(n_bars, n_assets)

    trade = list(generate_trades(universe, [lot], 1))[0]
    asset, lot, open_bar, close_bar = trade

    strategy = OneTradeStrategy(
        asset=asset, lot=lot, open_bar=open_bar, close_bar=close_bar,
    )
    strategy.run(universe, verbose=verbose)

    open_price = universe.prices.at[open_bar, asset]
    close_price = universe.prices.at[close_bar, asset]
    gain = lot * (close_price - open_price)
    duration = close_bar - open_bar

    assert strategy.history.order_index == np.array([0])
    assert strategy.history.trade_index == np.array([0])

    assert (strategy.history.assets == np.array([asset])).all()
    assert (strategy.history.lots == np.array([lot])).all()
    assert (strategy.history.open_bars == np.array([open_bar])).all()
    assert (strategy.history.close_bars == np.array([close_bar])).all()
    assert (strategy.history.durations == np.array([duration])).all()

    assert (strategy.history.open_prices == np.array([open_price])).all()
    assert (strategy.history.close_prices == np.array([close_price])).all()
    assert strategy.history.gains == np.array([gain])

    # TODO test transaction, wealth
