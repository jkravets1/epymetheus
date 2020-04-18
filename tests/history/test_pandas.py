import pytest

import numpy as np

from epymetheus import History
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader

columns = [
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


# --------------------------------------------------------------------------------


def test_columns():
    """
    Test if history.to_dataframe has the expected columns.
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)

    df_history = History(strategy).to_dataframe()

    assert df_history.index.name == 'order_id'
    assert list(df_history.columns) == columns


def test_value():
    """
    Test if value of history.to_dataframe is correct
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)

    history = History(strategy)
    df_history = history.to_dataframe()

    for c in columns:
        assert np.array_equal(df_history[c], history[c])
