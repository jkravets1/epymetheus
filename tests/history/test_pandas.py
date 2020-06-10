import pytest  # noqa: F401

import numpy as np
from numpy import array_equal
import pandas as pd
from pandas.testing import assert_index_equal

from epymetheus import History
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader

columns = pd.Index(
    [
        "trade_id",
        "asset",
        "lot",
        "open_bar",
        "close_bar",
        "shut_bar",
        "take",
        "stop",
        "pnl",
    ]
)


# --------------------------------------------------------------------------------


def test_type():
    """
    Test if history.to_dataframe is `pandas.DataFrame`.
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)

    df_history = History(strategy).to_dataframe()

    assert isinstance(df_history, pd.DataFrame)


def test_columns():
    """
    Test if history.to_dataframe has the expected columns.
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)

    df_history = History(strategy).to_dataframe()

    assert df_history.index.name == "order_id"
    assert_index_equal(df_history.columns, columns)


def test_index():
    """
    Test if value of history.to_dataframe is correct
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)

    history = History(strategy)
    df_history = history.to_dataframe()

    index_expected = pd.Index(range(df_history.index.size), name="order_id")
    assert_index_equal(df_history.index, index_expected)


def test_value():
    """
    Test if value of history.to_dataframe is correct
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)

    history = History(strategy)
    df_history = history.to_dataframe()

    for c in columns:
        assert array_equal(df_history[c], history[c])
