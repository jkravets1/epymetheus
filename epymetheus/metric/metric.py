# from abc import ABCMeta, abstractmethod

# import numpy as np


# # TODO
# # - sharpe
# # - sortino
# # - max_underwater
# # - beta
# # - alpha
# # - abs_exposure
# # - net_exposure


# class Metric(metaclass=ABCMeta):
#     """
#     Metric of backtesting.
#     """
#     @abstractmethod
#     def evaluate(self, strategy):
#         """
#         Evaluate metric of strategy.

#         Parameters
#         ----------
#         - strategy : TradeStrategy
#         """

#     def __call__(self, strategy, *args, **kwargs):
#         return self.evaluate(strategy, *args, **kwargs)


# class Volatility(Metric):
#     """
#     Return unbiased standard deviation of wealth per bar.

#     Returns
#     -------
#     volatility : float
#     """
#     def evaluate(self, strategy):
#         return np.std(np.diff(strategy.wealth.wealth), ddof=1)


# class SeriesDrawdown(Metric):
#     """
#     Return drawdown of the wealth from its cumulative max.

#     Note
#     ----
#     It is not a drawdown rate.

#     Returns
#     -------
#     series_drawdown : array, shape (n_bars, )

#     Examples
#     --------
#     >>> strategy.wealth
#     array([0, 1, 2, 1, 0])
#     >>> strategy.drop
#     array([0, 0, 0, -1, -2])
#     """
#     def evaluate(self, strategy):
#         return (
#             strategy.wealth.wealth
#             - np.maximum.accumulate(strategy.wealth.wealth)
#         )


# class MaxDrawdown(Metric):
#     """
#     Return maximum drawdown of the wealth from its cumulative max.

#     Note
#     ----
#     It is not a drawdown rate.

#     Returns
#     -------
#     max_drop : float
#         Maximum drop. always non-positive.

#     Examples
#     --------
#     >>> strategy.wealth
#     array([0, 1, 2, 1, 0])
#     >>> strategy.drop
#     array([0, 0, 0, -1, -2])
#     >>> strategy.max_drop
#     -2
#     """
#     def evaluate(self, strategy):
#         return min(SeriesDrop().evaluate(strategy))


# # TODO


# # class NetExposure(Metric):
# #     def evaluate(self, strategy):
# #         pass


# # class AbsExposure(Metric):
# #     def evaluate(self, strategy):
# #         pass


# def net_exposure(strategy):
#     """
#     Returns
#     -------
#     - net_exposure : array, shape (n_bars, )
#     """
#     net_position = np.cumsum(strategy.transaction_matrix, axis=0)
#     return np.sum(net_position * strategy.universe.prices.values, axis=1)


# def abs_exposure(strategy):
#     """
#     Returns
#     -------
#     - net_exposure : array, shape (n_bars, )
#     """
#     abs_position = np.abs(np.cumsum(strategy.transaction_matrix, axis=0))
#     return np.sum(abs_position * strategy.universe.prices.values, axis=1)
