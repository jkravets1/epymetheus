from abc import ABCMeta, abstractmethod
from functools import reduce

import numpy as np


# TODO
# - sortino
# - max_underwater
# - Factor coefficients
# - alpha
# - beta


def metric_from_name(name, **kwargs):
    """
    Initialize metric from a name.

    Parameters
    ----------
    - name : str
        Name of the metric to initialize.

    Returns
    -------
    metric : Metric
    """
    dict_metric = {
        "return": Return,
        "final_wealth": FinalWealth,
        "drawdown": Drawdown,
        "max_drawdown": MaxDrawdown,
        "volatility": Volatility,
        "sharpe_ratio": SharpeRatio,
        "tradewise_sharpe_ratio": TradewiseSharpeRatio,
        "exposure": Exposure,
    }

    if name not in dict_metric.keys():
        raise ValueError

    return dict_metric[name](**kwargs)


class Metric(metaclass=ABCMeta):
    """
    Base class of Metric.
    """

    @property
    @abstractmethod
    def name(self):
        """
        Return name of self.
        """

    @abstractmethod
    def result(self, strategy):
        """
        Evaluate metric of strategy.

        Parameters
        ----------
        - strategy : Strategy
        """

    def __call__(self, strategy, *args, **kwargs):
        return self.result(strategy, *args, **kwargs)


class Return(Metric):
    """
    Evaluate time-series of return.
    """

    def __init__(self, rate=False, **kwargs):
        super().__init__(**kwargs)
        self.rate = rate

    @property
    def name(self):
        return "return"

    def result(self, strategy):
        array_wealth = strategy.budget + strategy.wealth.wealth

        result = np.diff(array_wealth, prepend=strategy.budget)
        if self.rate:
            result /= np.roll(array_wealth, 1)

        return result


class FinalWealth(Metric):
    """
    Evaluate final wealth.

    Examples
    --------
    >>> strategy.wealth
    array([0.0, 1.0, 2.0, 1.0, 3.0])
    >>> FinalWealth().result(strategy)
    3.0
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        return "final_wealth"

    def result(self, strategy):
        array_wealth = strategy.wealth.wealth
        result = array_wealth[-1]

        return result


class Drawdown(Metric):
    """
    Evaluate series of drawdown rate/value of the wealth.

    Parameters
    ----------
    - rate : bool, default False
        If True, evaluate drawdown rate, that is, drawdown values divided by maximum values.
        If False, evaluate drawdown values.

    Returns
    -------
    drawdown : numpy.array, shape (n_bars, )

    Examples
    --------
    >>> strategy.wealth
    array([0.0, 1.0, 2.0, 1.0, 0.0])
    >>> Drawdown().result(strategy)
    array([0.0, 0.0, 0.0, -0.5, -1.0])
    >>> Drawdown(rate=False).result(strategy)
    array([0.0, 0.0, 0.0, -1.0, -2.0])
    """

    EPSILON = 10 ** -10

    def __init__(self, rate=False, **kwargs):
        super().__init__(**kwargs)
        self.rate = rate

    @property
    def name(self):
        return "drawdown"

    def result(self, strategy):
        array_wealth = strategy.wealth.wealth.values

        array_wealth_cummax = np.maximum.accumulate(array_wealth)
        drawdown = array_wealth - array_wealth_cummax

        if self.rate:
            # TODO This avoidance of divergence is too naive
            result = drawdown / (array_wealth_cummax + self.EPSILON)
        else:
            result = drawdown

        return result


class MaxDrawdown(Metric):
    """
    Evaluate maximum drawdown rate/value of the wealth.

    Parameters
    ----------
    - rate : bool, default False
        If True, evaluate maximum drawdown rate, that is, drawdown values divided by maximum values.
        If False, evaluate maximum drawdown values.

    Returns
    -------
    max_drawdown : float
        Maximum drop. always non-positive.

    Examples
    --------
    >>> strategy.wealth
    array([0, 1, 2, 1, 0])
    >>> strategy.drop
    array([0, 0, 0, -1, -2])
    >>> strategy.max_drop
    -2
    """

    def __init__(self, rate=False, **kwargs):
        super().__init__(**kwargs)
        self.rate = rate

    @property
    def name(self):
        return "max_drawdown"

    def result(self, strategy):
        array_drawdown = Drawdown(rate=self.rate).result(strategy)
        result = np.min(array_drawdown)

        return result


class Volatility(Metric):
    """
    Return standard deviation of pnl per bar.

    Parameters
    ----------
    - rate : bool, default False
        If True, volatility is evaluated for profit-loss rate.
        If False, volatility is evaluated for profit-loss.
    - ddof : int, default 1
        Delta degrees of freedom. The divisor used in calculations is N - ddof,
        where N represents the number of elements.

    Returns
    -------
    volatility : float
    """

    def __init__(self, rate=False, ddof=1, **kwargs):
        super().__init__(**kwargs)
        self.rate = rate
        self.ddof = ddof

    @property
    def name(self):
        return "volatility"

    def result(self, strategy):
        array_return = Return(rate=self.rate).result(strategy)
        result = np.std(array_return, ddof=self.ddof)

        return result


class SharpeRatio(Metric):
    """
    Evaluate sharpe ratio.

    Parameters
    ----------
    - rate : bool, default False
        If True, return and risk are evaluated using pnl rate.
        If False, return and risk are evaluated using pnl.
    - risk_free_return : float, default 0.0
        Risk free return.

    Returns
    -------
    sharpe_ratio : float
    """

    EPSILON = 10 ** -10

    def __init__(self, rate=False, risk_free_return=0.0, **kwargs):
        super().__init__(**kwargs)
        self.rate = rate
        self.risk_free_return = risk_free_return

    @property
    def name(self):
        return "sharpe_ratio"

    def result(self, strategy):
        avg_return = np.mean(Return(rate=self.rate).result(strategy))
        std_return = Volatility(rate=self.rate).result(strategy)
        result = (avg_return - self.risk_free_return) / std_return

        return result


class TradewiseSharpeRatio(Metric):
    """
    Evaluate Sharpe ratio for profit-loss of each trade.

    Returns
    -------
    tradewise_sharpe_ratio : float
    """

    EPSILON = 10 ** -10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        return "tradewise_sharpe_ratio"

    def result(self, strategy):
        array_pnl = strategy.history.to_dataframe().groupby("trade_id").agg(sum)["pnl"]
        avg_pnl = np.mean(array_pnl)
        std_pnl = np.std(array_pnl)  # TODO parameter ddof
        result = avg_pnl / max(std_pnl, self.EPSILON)

        return result


class Exposure(Metric):
    """
    Evaluate net exposure.

    Parameters
    ----------
    - net : bool, default False
        If True, evaluate net exposure.
        If False, evaluate absolute exposure.

    Returns
    -------
    exposure : numpy.array, shape (n_bars, )
    """

    def __init__(self, net=True, **kwargs):
        super().__init__(**kwargs)
        self.net = net

    @property
    def name(self):
        return "net_exposure"

    def result(self, strategy):
        exposures = (
            trade.series_exposure(universe, net=self.net) for trade in strategy.trades
        )
        return reduce(np.add, exposures)


# class Beta(Metric):
#     """
#     Evaluate beta.

#     Parameters
#     ----------
#     - benchmark : strategy
#     - rate : bool
#     """

#     def __init__(self, benchmark, rate=False, **kwargs):
#         super().__init__(**kwargs)
#         self.rate = rate
#         self.benchmark = benchmark

#     @property
#     def name(self):
#         return "beta"

#     def result(self, strategy):
#         if not self.benchmark.is_run:
#             self.benchmark.run(strategy)

#         array_return_s = Return(rate=self.rate).result(strategy)
#         array_return_b = Return(rate=self.rate).result(benchmark)
#         cov = np.cov(array_return_s, array_return_b)[0, 1]
#         var = np.var(array_return_b)
#         result = cov / var

#         return result
