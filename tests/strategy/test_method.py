import pytest

import pandas as pd

from epymetheus import Trade, TradeStrategy, Universe
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


params_trades = [trades]
params_universe = [universe]
params_verbose = [True, False]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('trades', params_trades)
@pytest.mark.parametrize('universe', params_universe)
@pytest.mark.parametrize('verbose', params_verbose)
def test_generate(trades, universe, verbose):
    strategy = DeterminedTrader(trades=trades)
    strategy.run(universe, verbose=verbose)

    assert strategy.trades == trades


@pytest.mark.parametrize('trades', [trades])
@pytest.mark.parametrize('universe', [universe])
@pytest.mark.parametrize('verbose', params_verbose)
def test_execute(trades, universe, verbose):
    strategy = DeterminedTrader(trades=trades)
    strategy.run(universe, verbose=verbose)

    close_bar_expected = [
        trade.execute(universe).close_bar for trade in strategy.trades
    ]
    pnl_expected = [
        trade.execute(universe).pnl for trade in strategy.trades
    ]

    assert [trade.close_bar for trade in strategy.trades] == close_bar_expected
    assert [trade.pnl for trade in strategy.trades] == pnl_expected
