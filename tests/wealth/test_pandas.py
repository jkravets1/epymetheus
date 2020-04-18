import pytest  # noqa: F401

import numpy as np

from epymetheus import Wealth
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


def test_series_value():
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    series_wealth = wealth.to_series()

    assert np.array_equal(series_wealth, wealth['wealth'])


def test_dataframe_columns():
    """
    Test if history.to_dataframe has the expected columns.
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    df_wealth = wealth.to_dataframe()

    assert df_wealth.index.name == 'bars'
    assert list(df_wealth.columns) == ['wealth']


def test_dataframe_value():
    """
    Test if value of history.to_dataframe is correct
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    df_wealth = wealth.to_dataframe()

    assert np.array_equal(df_wealth['wealth'], wealth.wealth)
