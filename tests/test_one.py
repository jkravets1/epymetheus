import pytest

import random
import numpy as np

from epymetheus import TradeStrategy
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader, SingleTradeStrategy


params_seed = [42]
params_n_bars = [100, 1000]
params_n_assets = [3, 10, 100]
params_lot = [0.0, 1, 1.23, -1.23, 123.4, -123.4]
params_verbose = [True, False]


def one_random_trade(universe, max_n_orders, seed):
    """
    Generate a single trade randomly.

    Returns
    -------
    trade : Trade
    """
    random_trader = RandomTrader(n_trades=1, max_n_orders=max_n_orders, seed=seed)
    trade = random_trader.run(universe).trades[0]
    return trade


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('lot', params_lot)
@pytest.mark.parametrize('verbose', params_verbose)
def test_one(seed, n_bars, n_assets, lot, verbose):
    universe = make_randomwalk(n_bars=n_bars, n_assets=n_assets, seed=seed)

    trade = one_random_trade(universe, max_n_orders=1, seed=seed)

    asset = trade.asset
    lot = trade.lot
    open_bar = trade.open_bar
    shut_bar = trade.shut_bar
    open_price = universe.prices.at[open_bar, asset[0]]
    close_price = universe.prices.at[shut_bar, asset[0]]
    gain = lot * (close_price - open_price)
    duration = shut_bar - open_bar

    strategy = SingleTradeStrategy(trade=trade).run(universe, verbose=verbose)

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
