# SimpleMeanReversion
A simple Mean Reversion strategy that buys stocks for a month with
the lowest percentile one month returns and sells the highest percentile returns.

Parameters
----------
- percentile : float
    The threshold to buy or sell.
    E.g. If 0.1, buy/sell stocks with returns of lowest/highest 10%.

## Parameters used
- **percentile** : 0.1

## Universe
- **Universe** : JP Equity
- **Period** : 2000/01/01 - 2018/12/31 (6939 days)

|wealth and exposure|record|
|:-:|:-:|
|![wealth](wealth.png "")|![record](record.png "")|

## Overview
- **fin wealth** : 4.45202
- **max drop** : -2.49837
- **avg gain** : 0.01899
- **med gain** : 0.01899

## Trade statistics
- **num trade** : 452
- **avg duration** : 29 days
- **med duration** : 30 days
- **max duration** : 30 days
- **min duration** : 27 days

## Win and lose
|        |   win   |  lose   |
|--------|--------:|--------:|
|num     |153.00000|133.00000|
|avg gain|  0.17061| -0.15543|
|med gain|  0.11824| -0.12503|
|max gain|  0.93417| -0.00028|
|min gain|  0.00193| -0.85377|

Backtest runtime : 3.4 sec