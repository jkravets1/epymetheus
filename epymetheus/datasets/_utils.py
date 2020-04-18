import pandas as pd


def ffill_and_cut(series, begin_date):
    """
    Examples
    --------
    >>> series
    1999-12-30  0
    2000-01-02  1
    2000-01-03  2
    2000-01-05  3
    >>> _fill_and_cut(series, begin_date='2000-01-01')
    2000-01-01  0
    2000-01-02  1
    2000-01-03  2
    2000-01-04  2
    2000-01-05  3
    """
    return (
        series
        .reindex(
            pd.date_range(series.index[0], series.index[-1]),
            method='ffill',
        )
        .ffill()
        .reindex(
            pd.date_range(begin_date, series.index[-1])
        )
    )
