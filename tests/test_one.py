import pytest

import random
import numpy as np

from epymetheus import TradeStrategy


params_seed = [42]
params_n_bars = [100, 1000]
params_n_assets = [3, 10, 100]
params_lot = [0.0, 1, 1.23, -1.23, 123.4, -123.4]
params_verbose = [True, False]


class OneTradeStrategy(TradeStrategy):
    """
    Yield a single trade.
    """
    def logic(self, universe, trade):
        yield trade


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('lot', params_lot)
@pytest.mark.parametrize('verbose', params_verbose)
def test_one(seed, n_bars, n_assets, lot, verbose, make_randomuniverse, generate_trades):
    np.random.seed(seed)
    random.seed(seed)

    universe = make_randomuniverse(n_bars, n_assets)

    trade = list(generate_trades(universe, n_trades=1, max_n_orders=1))[0]
    asset = trade.asset
    lot = trade.lot
    open_bar = trade.open_bar
    shut_bar = trade.shut_bar
    open_price = universe.prices.at[open_bar, asset[0]]
    close_price = universe.prices.at[shut_bar, asset[0]]
    gain = lot * (close_price - open_price)
    duration = shut_bar - open_bar

    strategy = OneTradeStrategy(trade=trade).run(universe, verbose=verbose)

    assert strategy.history.order_index == np.array([0])
    assert strategy.history.trade_index == np.array([0])

    assert (strategy.history.assets == np.array(asset)).all()
    assert (strategy.history.lots == np.array([lot])).all()
    assert (strategy.history.open_bars == np.array([open_bar])).all()
    assert (strategy.history.close_bars == np.array([shut_bar])).all()
    assert (strategy.history.durations == np.array([duration])).all()

    assert (strategy.history.open_prices == np.array([open_price])).all()
    assert (strategy.history.close_prices == np.array([close_price])).all()
    assert strategy.history.gains == np.array([gain])

    # TODO test transaction, wealth
