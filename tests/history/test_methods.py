import pytest  # noqa: F401

import numpy as np
from numpy import array_equal
import pandas as pd
from pandas.testing import assert_index_equal, assert_frame_equal

from epymetheus import History
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader


class TestToDataFrame:
    """
    Test for `History.to_dataframe()`.
    """

    def _get_history(self):
        strategy = RandomTrader(seed=42).run(make_randomwalk(42))
        return History(strategy)

    def _get_df_history(self):
        strategy = RandomTrader(seed=42).run(make_randomwalk(42))
        return History(strategy).to_dataframe()

    def test_pandas_init(self):
        """
        Test if `history.to_dataframe() == pd.DataFrame(history)`.
        """
        history = self._get_history()
        result0 = history.to_dataframe()
        result1 = pd.DataFrame(history).set_index("order_id")
        assert_frame_equal(result0, result1)

    def test_type(self):
        """
        Test if history.to_dataframe is `pandas.DataFrame`.
        """
        df_history = self._get_df_history()
        assert isinstance(df_history, pd.DataFrame)

    def test_columns(self):
        """
        Test if history.to_dataframe has the expected columns.
        """
        df_history = self._get_df_history()
        expected = pd.Index(
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
        assert df_history.index.name == "order_id"
        assert_index_equal(df_history.columns, expected)

    def test_index(self):
        """
        Test if value of history.to_dataframe is correct.
        """
        df_history = self._get_df_history()
        expected = pd.Index(range(df_history.index.size), name="order_id")
        assert_index_equal(df_history.index, expected)

    def test_value(self):
        """
        Test if value of history.to_dataframe is correct.
        """
        history = self._get_history()
        df_history = self._get_df_history()
        for c in df_history.columns:
            assert array_equal(df_history[c], history[c])
