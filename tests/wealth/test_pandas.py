import pytest  # noqa: F401

import numpy as np
from numpy import array_equal
import pandas as pd
from pandas.testing import assert_index_equal, assert_series_equal

from epymetheus import Wealth
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader


# --------------------------------------------------------------------------------


def test_series_type():
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    series_wealth = wealth.to_series()

    assert isinstance(series_wealth, pd.Series)


def test_series_value():
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    series_wealth = wealth.to_series()

    assert np.array_equal(series_wealth, wealth['wealth'])


def test_dataframe_type():
    """
    Test if history.to_dataframe is `pandas.DataFrame`.
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    df_wealth = wealth.to_dataframe()

    assert isinstance(df_wealth, pd.DataFrame)


def test_dataframe_columns():
    """
    Test if history.to_dataframe has the expected columns.
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    df_wealth = wealth.to_dataframe()

    assert df_wealth.index.name == 'bars'
    assert_index_equal(df_wealth.columns, pd.Index(['wealth']))


def test_dataframe_index():
    """
    Test if value of history.to_dataframe is correct
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    df_wealth = wealth.to_dataframe()

    assert_index_equal(df_wealth.index, universe.bars, check_names=False)

def test_dataframe_value():
    """
    Test if value of history.to_dataframe is correct
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)
    wealth = Wealth(strategy)
    df_wealth = wealth.to_dataframe()

    assert array_equal(df_wealth['wealth'].values, wealth.wealth)
