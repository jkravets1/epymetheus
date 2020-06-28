# Epymetheus: Python library for multi-asset backtesting

[![version](https://img.shields.io/pypi/v/epymetheus.svg)](https://pypi.org/project/epymetheus/)
[![Build Status](https://travis-ci.com/simaki/epymetheus.svg?branch=master)](https://travis-ci.com/simaki/epymetheus)
[![codecov](https://codecov.io/gh/simaki/epymetheus/branch/master/graph/badge.svg)](https://codecov.io/gh/simaki/epymetheus)
[![dl](https://img.shields.io/pypi/dm/epymetheus)](https://pypi.org/project/epymetheus/)
[![LICENSE](https://img.shields.io/github/license/simaki/epymetheus)](LICENSE)

![wealth](examples/howto/wealth.png)

## Introduction

This library provides simple and efficient framework of backtesting.

### Features

1. **Simple and Intuitive API**: The API is minimally organized so that you can focus on your idea. Trade strategy can be easily coded in a `TradeStrategy` class and backtest is consistently carried out by its `run()`, `evaluate()` methods.
2. **Seamless to Pandas**: Input historical data is based on Pandas DataFrame and backtesting results - trade history, cumulated wealth, drawdown, exposure and so forth - can be converted to Pandas format by the methods `to_series()` or `to_dataframe()` right away. You can view, manipulate and plot your data by the familliar pandas methods.
3. **Extensible with Other Frameworks**: Epymetheus only provides a framework, so that it can be readily integrated with other libraries for machine learning, econometrics, technical indicators, derivative pricing models and so forth.
4. **Efficient Computation**: Backtesting engine are boosted by numpy. You can quickly give your own idea a try.
5. **Fully tested**: The library is thoroughly tested with 100% test coverage for multiple Python versions.

## Installation

```sh
$ pip install epymetheus
```

## How to use

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/simaki/fracdiff/blob/master/examples/howto/howto.ipynb)

Let's construct your own strategy by subclassing `TradeStrategy`.

```python
from epymetheus import Trade, TradeStrategy


class MyStrategy(TradeStrategy):
    """
    This is my favorite strategy.

    Parameters
    ----------
    - my_parameter : float
        My awesome parameter.
    """
    def __init__(self, my_parameter):
        self.my_parameter = my_parameter

    def logic(self, universe):
        ...
        yield Trade(...)


strategy = MyStrategy(my_parameter=0.1)
```

The strategy can be readily applied to any `Universe`.

```python
from epymetheus import Universe

prices = ...  # Fetch historical prices of US equities
universe = Universe(prices)

strategy.run(universe)
# Running ...
# Generating 454 trades (2018-12-31) ... Done. (Runtime : 0.45 sec)
# Executing 454 trades ... Done. (Runtime : 0.73 sec)
# Done. (Runtime : 1.17 sec)
```

Now the result can be evaluated as the attributes of `strategy`.
You can plot the wealth right away:

```python
df_wealth = strategy.wealth.to_dataframe()

df_wealth.plot()
```

![wealth](examples/howto/wealth.png)

You can also inspect the exposure as:

```python
net_exposure = pd.Series(strategy.net_exposure)
net_exposure.plot()
```

![exposure](examples/howto/exposure.png)

Profit-loss distribution can be accessed by:

```python
plt.hist(strategy.history.pnl)
```

![pnl](examples/howto/pnl.png)

Detailed trade history can be viewed as:

```python
strategy.history.to_dataframe()

# or: pandas.DataFrame(strategy.history)
```

|   order_id |   trade_id | asset   |           lot | open_bar    | close_bar   | shut_bar    |   take |   stop |          pnl |
|-----------:|-----------:|:--------|--------------:|:------------|:------------|:------------|-------:|-------:|-------------:|
|          0 |          0 | BRK-A   |     0.227273  | 2000-02-29  | 2000-08-29  | 2000-08-29  |   5000 |  -1000 |  3113.64     |
|          1 |          1 | JNJ     |   471.411     | 2000-02-29  | 2000-08-29  | 2000-08-29  |   5000 |  -1000 |  3097.16     |
|          2 |          2 | PG      |   657.239     | 2000-03-31  | 2000-09-30  | 2000-09-30  |   5000 |  -1000 |  2061.64     |
|          3 |          3 | AMZN    |   149.254     | 2000-03-31  | 2000-04-12  | 2000-09-30  |   5000 |  -1000 | -1585.82     |
|          4 |          4 | MSFT    |   446.908     | 2000-04-28  | 2000-05-25  | 2000-10-28  |   5000 |  -1000 | -1182.8      |

## Integrations

Strategies may be integrated with:

- **Machine Learning**: [scikit-learn](https://github.com/scikit-learn/scikit-learn), [TensorFlow](https://github.com/tensorflow/tensorflow), [PyTorch](https://github.com/pytorch/pytorch), etc.
- **Econometrics**: [statsmodels](https://github.com/statsmodels/statsmodels), etc.
- **Technical Indicators**: [TA-Lib](https://github.com/mrjbq7/ta-lib), etc.
- **Derivative Pricing**: [TF Quant Finance](https://github.com/google/tf-quant-finance), etc.
