# Epymetheus

[![version](https://img.shields.io/pypi/v/epymetheus.svg)](https://pypi.org/project/epymetheus/)
[![Build Status](https://travis-ci.org/simaki/epymetheus.svg?branch=master)](https://travis-ci.com/simaki/epymetheus)
[![LICENSE](https://img.shields.io/github/license/simaki/epymetheus)](LICENSE)

Python framework for multi-asset backtesting.

![wealth](./sample/SimpleMeanReversion/wealth.png)

## Installation

```sh
$ pip install epymetheus
```

## Features

- Multi-asset backtesting
- Financial data scraping

## Usage

```python
import epymetheus as ep


class MyTradeStrategy(ep.TradeStrategy):
    """This is my favorite strategy."""
    def logic(self, universe, my_parameter):
        ...
        yield trade


def main():
    n225 = ep.Universe.read_directory('./Nikkei 225/')
    my_strategy = MyTradeStrategy(my_parameter=0.01)
    my_strategy.run(universe=n225)


if __name__ == '__main__':
    main()
```

- [Sample result](https://github.com/simaki/epymetheus/blob/master/sample/SimpleMeanReversion/summary.md)

## Todo

- commission
- initial wealth
- alpha, beta to benchmark

maybe...
- pdf output
- monthly report
- user-defined measure evaluation
- user-defined data export
- prometest (look-forward tester)
