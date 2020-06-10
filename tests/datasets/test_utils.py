import pytest  # noqa: F401

import pandas as pd

from epymetheus.datasets._utils import ffill_and_cut


def test_ffill_and_cut():
    from pandas.testing import assert_series_equal

    series = pd.Series(
        {
            pd.Timestamp("1999-12-30"): 0,
            pd.Timestamp("2000-01-02"): 1,
            pd.Timestamp("2000-01-03"): 2,
            pd.Timestamp("2000-01-05"): 3,
        }
    )
    series_expected = pd.Series(
        {
            pd.Timestamp("2000-01-01"): 0,
            pd.Timestamp("2000-01-02"): 1,
            pd.Timestamp("2000-01-03"): 2,
            pd.Timestamp("2000-01-04"): 2,
            pd.Timestamp("2000-01-05"): 3,
        }
    )

    assert_series_equal(ffill_and_cut(series, "2000-01-01"), series_expected)
