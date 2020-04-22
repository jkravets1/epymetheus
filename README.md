# Epymetheus

[![version](https://img.shields.io/pypi/v/epymetheus.svg)](https://pypi.org/project/epymetheus/)
[![Build Status](https://travis-ci.com/simaki/epymetheus.svg?branch=master)](https://travis-ci.com/simaki/epymetheus)
[![codecov](https://codecov.io/gh/simaki/epymetheus/branch/master/graph/badge.svg)](https://codecov.io/gh/simaki/epymetheus)
[![dl](https://img.shields.io/pypi/dm/epymetheus)](https://pypi.org/project/epymetheus/)
[![LICENSE](https://img.shields.io/github/license/simaki/epymetheus)](LICENSE)

Python library for multi-asset backtesting.

![wealth](examples/howto/wealth.png)

## Installation

```sh
$ pip install epymetheus
```

## Features

- Multi-asset backtesting

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

![pnl](examples/howto/gains.png)

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

