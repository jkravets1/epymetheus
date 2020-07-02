# Epymetheus: Python Library for Multi-asset Backtesting

[![python versions](https://img.shields.io/pypi/pyversions/epymetheus.svg)](https://pypi.org/project/epymetheus/)
[![version](https://img.shields.io/pypi/v/epymetheus.svg)](https://pypi.org/project/epymetheus/)
[![build status](https://travis-ci.com/simaki/epymetheus.svg?branch=master)](https://travis-ci.com/simaki/epymetheus)
[![codecov](https://codecov.io/gh/simaki/epymetheus/branch/master/graph/badge.svg)](https://codecov.io/gh/simaki/epymetheus)
[![dl](https://img.shields.io/pypi/dm/epymetheus)](https://pypi.org/project/epymetheus/)
[![LICENSE](https://img.shields.io/github/license/simaki/epymetheus)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![wealth](examples/howto/wealth.png)

## Introduction

Epymetheus is a Python library for multi-asset backtesting.
It provides end-to-end framework that lets analysts build and try out their trade strategy right away.

### Features

1. **Simple and Intuitive API**: The API is minimally organized so that you can focus on your idea. Trade `Strategy` can be readily coded and its backtesting is consistently carried out by its methods `run()` and `evaluate()`.
2. **Seamless connection to [Pandas](https://github.com/pandas-dev/pandas)**: You can just put in pandas DataFrame as an input historical data. Backtesting results can be quickly converted to Pandas format so that you can view, analyze and plot results by the familliar Pandas methods.
3. **Extensiblity with Other Frameworks**: Epymetheus only provides a framework. Strategy can be readily built with other libraries for machine learning, econometrics, technical indicators, derivative pricing models and so forth.
4. **Efficient Computation**: Backtesting engine is boosted by numpy. You can give your own idea a quick try.
5. **Full Test Coverage**: Library is thoroughly tested with 100% test coverage for multiple Python versions.

### Modules

1. **[Strategy](https://github.com/simaki/epymetheus/tree/master/epymetheus/strategy)**: A strategy encodes your own trading rules. The [`benchmarks`](https://github.com/simaki/epymetheus/tree/master/epymetheus/benchmarks) provide standard strategies to be compared with.
2. **[Universe](https://github.com/simaki/epymetheus/tree/master/epymetheus/universe)**: A universe stores historical prices of a set of securities. The [`datasets`](https://github.com/simaki/epymetheus/tree/master/epymetheus/datasets) provides sample universe like Brownian stock prices and blue chips in US.
3. **[History](https://github.com/simaki/epymetheus/tree/master/epymetheus/history)**: A history stores the assets, lots, profit/loss of each trade yielded. Easily converted into Pandas DataFrame.
4. **[Metric](https://github.com/simaki/epymetheus/tree/master/epymetheus/metric)**: A metric is a function to assess the performance of your strategy. Available metrics include: final wealth, maximum drawdown, Sharpe ratio and so forth.

### Integrations

Strategies may be integrated with:

- **Machine Learning**: [scikit-learn](https://github.com/scikit-learn/scikit-learn), [TensorFlow](https://github.com/tensorflow/tensorflow), [PyTorch](https://github.com/pytorch/pytorch), etc.
- **Econometrics**: [statsmodels](https://github.com/statsmodels/statsmodels), etc.
- **Technical Indicators**: [TA-Lib](https://github.com/mrjbq7/ta-lib), etc.
- **Derivative Pricing**: [TF Quant Finance](https://github.com/google/tf-quant-finance), etc.

## Installation

```sh
$ pip install epymetheus
```

## How to use

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/simaki/epymetheus/blob/master/examples/howto/howto.ipynb)

Let's construct your own `Strategy`.

```python
from epymetheus import Trade, Strategy


class MyStrategy(Strategy):
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

Now your strategy can be applied to any `Universe`.

```python
from epymetheus import Universe

prices = ...  # Fetch historical prices of US equities as pandas.DataFrame
universe = Universe(prices)

strategy.run(universe)
# Running ...
# Generating 454 trades (2018-12-31) ... Done. (Runtime : 0.45 sec)
# Executing 454 trades ... Done. (Runtime : 0.73 sec)
# Done. (Runtime : 1.17 sec)
```

Now the results can be accessed as the attributes of `strategy`.
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
