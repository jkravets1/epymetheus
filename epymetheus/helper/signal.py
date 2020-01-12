import pandas as pd
import datetime
from itertools import compress, chain
from typing import Union, Iterable

from epymetheus.core.api import Universe


def trade_begin_dates(
    universe: Universe,
    train_period,
    trade_period
):
    """Yield begin dates of trade periods."""
    d = universe.begin_date + train_period
    while d + trade_period <= universe.end_date:
        yield d
        d += trade_period


def cross(
    array: Union[pd.Series, pd.DataFrame],
    direction='up'
):
    """
    True if the value crosses 0 upward or downward.
    Parameters
    ----------
    array : pandas.Series or pandas.DataFrame
    direction : {'up', 'down'}, default 'up'
        Cross upward or downward.
    """
    if isinstance(array, pd.core.series.Series):
        if direction == 'up':
            return (array > 0) & (array.shift() <= 0)
        if direction == 'down':
            return (array < 0) & (array.shift() >= 0)
        raise ValueError("direction must be in {'up', 'down'},"
                         "but {} given".format(direction))
    if isinstance(array, pd.core.frame.DataFrame):
        return pd.DataFrame({
            c: cross(array[c], direction=direction)
            for c in array.columns
        })
    raise TypeError


def timing(
    series_open: pd.Series,
    series_close: pd.Series
):
    """
    Return list of (begin date, end date) from open and close signals.
    Parameters
    ----------
    - series_open : pd.Series
        True if signal to open a trade is on, otherwise False.
    - series_close : pd.Series
        True if signal to close a trade is on, otherwise False.
    Returns
    -------
    List of (date_open, date_close)
    where date_open and date_close are dates to open and close each trade,
    Examples
    --------
    >>> series_open
    2019-01-01  False
    2019-01-02  True
    2019-01-03  False
    2019-01-04  True
    2019-01-05  False
    ...         ...
    >>> series_close
    2019-01-01  True
    2019-01-02  False
    2019-01-03  False
    2019-01-04  False
    2019-01-05  True
    ...         ...
    >>> timing_from_openclose(series_open, series_close)
    [(datetime.date(2019, 1, 2), datetime.date(2019, 1, 5)), ...]
    """
    signal_open = compress(series_open.index, series_open)
    signal_close = compress(series_close.index, series_close)

    sentinel = datetime.date(datetime.MINYEAR, 1, 1)

    timing = []
    date_now = next(signal_open, sentinel)
    opening = False

    while True:
        if opening:
            date_next = next(signal_close, sentinel)
            if date_next > date_now:
                timing.append((date_now, date_next))
                date_now = date_next
                opening = False
        else:
            date_next = next(signal_open, sentinel)
            if date_next > date_now:
                date_now = date_next
                opening = True

        if date_next == sentinel:
            return timing


def timing_flag(
    opens: Iterable[pd.Series],
    closes: Iterable[pd.Series]
):
    """
    Return timings and which signals were caught.
    Returns
    -------
    List of (begin_date, end_date, flag_open, flag_close)
        flag_open [flag_close] is index of signal that was
        caught to open [close] each trade.
    """
    signal_open = chain.from_iterable(
        [(date, flag) for date in compress(series.index, series)]
        for flag, series in enumerate(opens)
    )
    signal_close = chain.from_iterable(
        [(date, flag) for date in compress(series.index, series)]
        for flag, series in enumerate(closes)
    )
    signal_open = iter(sorted(
        list(signal_open), key=lambda date_flag: date_flag[0]
    ))
    signal_close = iter(sorted(
        list(signal_close), key=lambda date_flag: date_flag[0]
    ))

    sentinel = (datetime.date(datetime.MINYEAR, 1, 1), None)

    timing_flag = []
    date_now, flag_open = next(signal_open, sentinel)
    opening = False

    while True:
        if opening:
            (date_next, flag_close) = next(signal_close, sentinel)
            if date_next > date_now:
                timing_flag.append(
                    (date_now, date_next, flag_open, flag_close)
                )
                date_now = date_next
                opening = False
        else:
            (date_next, flag_open) = next(signal_open, sentinel)
            if date_next > date_now:
                date_now = date_next
                opening = True

        if date_next == sentinel[0]:
            return timing_flag
