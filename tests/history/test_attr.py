import pytest

import numpy as np
import pandas as pd
from epymetheus import Trade, History, Universe
from epymetheus.benchmarks import DeterminedTrader

trade0 = Trade(
    asset=['Asset0', 'Asset1'],
    lot=[1, 2],
    open_bar='Bar0',
    shut_bar='Bar1',
    take=3,
    stop=4,
)
trade1 = Trade(
    asset=['Asset2', 'Asset3'],
    lot=[5, 6],
    open_bar='Bar2',
    shut_bar='Bar3',
    take=7,
    stop=8,
)

trades = [trade0, trade1]

universe = Universe(
    prices=pd.DataFrame({
        f'Asset{n}': 0 for n in range(4)
    }, index=[f'Bar{n}' for n in range(4)])
)


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('trades', [trades])
def test_trade_keys(trades):
    """
    Test if history has the expected columns.
    """
    strategy = DeterminedTrader(trades=trades)
    strategy.run(universe)  # Run to prevent NotRunError
    history = History(strategy)

    assert list(history.keys()) == [
        'order_id',
        'trade_id',
        'asset',
        'lot',
        'open_bar',
        'close_bar',
        'shut_bar',
        'take',
        'stop',
        'pnl',
    ]


@pytest.mark.parametrize('trades', [trades])
def test_trade_id(trades):
    strategy = DeterminedTrader(trades=trades)
    strategy.run(universe)  # Run to prevent NotRunError
    history = History(strategy)

    assert np.array_equal(history.trade_id, [0, 0, 1, 1])


@pytest.mark.parametrize('trades', [trades])
def test_order_id(trades):
    strategy = DeterminedTrader(trades=trades)
    strategy.run(universe)  # Run to prevent NotRunError
    history = History(strategy)

    assert np.array_equal(history.order_id, [0, 1, 2, 3])


@pytest.mark.parametrize('trades', [trades])
def test_asset(trades):
    strategy = DeterminedTrader(trades=trades)
    strategy.run(universe)  # Run to prevent NotRunError
    history = History(strategy)

    assert np.array_equal(history.asset, ['Asset0', 'Asset1', 'Asset2', 'Asset3'])


@pytest.mark.parametrize('trades', [trades])
def test_open_bar(trades):
    strategy = DeterminedTrader(trades=trades)
    strategy.run(universe)  # Run to prevent NotRunError
    history = History(strategy)

    assert np.array_equal(history.open_bar, ['Bar0', 'Bar0', 'Bar2', 'Bar2'])


@pytest.mark.parametrize('trades', [trades])
def test_shut_bar(trades):
    strategy = DeterminedTrader(trades=trades)
    strategy.run(universe)  # Run to prevent NotRunError
    history = History(strategy)

    assert np.array_equal(history.shut_bar, ['Bar1', 'Bar1', 'Bar3', 'Bar3'])
