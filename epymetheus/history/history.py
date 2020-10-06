import numpy as np
import pandas as pd

from epymetheus.exceptions import NotRunError
from epymetheus.utils import TradeResult


class History(TradeResult):
    """
    Represent trade history.

    Attributes
    ----------
    - order_id : numpy.array, shape (n_orders, )
        Indices of orders.
    - trade_id : numpy.array, shape (n_orders, )
        Indices of trades.
    - asset : numpy.array, shape (n_orders, )
        Assets to trade.
    - lot : numpy.array, shape (n_orders, )
        Lots to trade.
    - open_bar : numpy.array, shape (n_orders, )
        Bar to open each trade.
    - close_bar : numpy.array, shape (n_orders, )
        Bar to close each trade.
    - take : numpy.array, shape (n_orders, )
        Profit-take of each trade.
    - stop : numpy.array, shape (n_orders, )
        Stop-loss of each trade.
    - pnl : numpy.array, shape (n_orders, )
        Profit loss of each order.
    """

    @classmethod
    def from_strategy(cls, strategy):
        """
        Initialize self from strategy.

        Parameters
        ----------
        - strategy : Strategy

        Returns
        -------
        history : History
        """
        if not strategy.is_run:
            raise NotRunError("Strategy has not been run")

        return cls(
            order_id=cls._get_order_id(strategy),
            trade_id=cls._get_trade_id(strategy),
            asset=cls._get_asset(strategy),
            lot=cls._get_lot(strategy),
            open_bar=cls._get_open_bar(strategy),
            close_bar=cls._get_close_bar(strategy),
            shut_bar=cls._get_shut_bar(strategy),
            take=cls._get_take(strategy),
            stop=cls._get_stop(strategy),
            pnl=cls._get_pnl(strategy),
        )

    def to_dataframe(self, copy=False):
        """
        Represent self as `pandas.DataFrame`.

        Parameters
        ----------
        - copy : bool, default False
            Copy input data.

        Returns
        -------
        df_wealth : pandas.DataFrame
        """
        return pd.DataFrame(self, copy=copy).set_index("order_id")

    @staticmethod
    def _get_order_id(strategy):
        """
        Return order_id of each order.

        Returns
        -------
        array_order_id : array, shape (n_orders, )
            array([0, 1, ..., n_orders - 1])

        Examples
        --------
        # >>> strategy.trades = [
        # ...     Trade(asset=['Asset0', 'Asset1'], ...),
        # ...     Trade(asset=['Asset2'], ...),
        # ... ]
        # >>> History()._get_order_id(strategy)
        # array([  0  1  2])
        """
        return np.arange(strategy.n_orders)

    @staticmethod
    def _get_trade_id(strategy):
        """
        Return trade_id of each order.

        Returns
        -------
        array_trade_id : array, shape (n_orders, )

        Examples
        --------
        # >>> strategy.trades = [
        # ...     Trade(asset=['Asset0', 'Asset1'], ...),
        # ...     Trade(asset=['Asset2'], ...),
        # ... ]
        # >>> History()._get_trade_id(strategy)
        # array([  0  0  1])
        """
        return np.repeat(
            np.arange(strategy.n_trades), [trade.n_orders for trade in strategy.trades]
        )

    @staticmethod
    def _get_asset(strategy):
        """
        Return asset of each order.

        Returns
        -------
        array_asset : array, shape (n_orders, )

        Examples
        --------
        # >>> strategy.trades = [
        # ...     Trade(asset=['Asset0', 'Asset1'], ...),
        # ...     Trade(asset=['Asset2'], ...),
        # ... ]
        # >>> History()._get_asset(strategy)
        # array([  'Asset0'  'Asset1'  'Asset2'])
        """
        return np.concatenate([trade.array_asset for trade in strategy.trades])

    @staticmethod
    def _get_lot(strategy):
        """
        Return lot of each order.

        Returns
        -------
        array_lot : array, shape (n_orders, )

        Examples
        --------
        # >>> strategy.trades = [
        # ...     Trade(lot=[1, -2], ...),
        # ...     Trade(lot=[3], ...),
        # ... ]
        # >>> History()._get_lot(strategy)
        # array([  1 -2  3])
        """
        return np.concatenate([trade.array_lot for trade in strategy.trades])

    @staticmethod
    def _get_open_bar(strategy):
        """
        Return open_bar of each order.

        Returns
        -------
        array_open_bar : array, shape (n_orders, )

        Examples
        --------
        # >>> strategy.trades = [
        # ...     Trade(open_bar='Bar0', asset=['Asset0', 'Asset1'], ...),
        # ...     Trade(open_bar='Bar1', asset=['Asset2'], ...),
        # ... ]
        # >>> History()._get_open_bar(strategy)
        # array([  'Bar0'  'Bar0'  'Bar1'])
        """
        return np.repeat(
            [trade.open_bar for trade in strategy.trades],
            [trade.n_orders for trade in strategy.trades],
        )

    @staticmethod
    def _get_close_bar(strategy):
        """
        Return close_bar of each order.

        Returns
        -------
        array_close_bar : array, shape (n_orders, )

        Examples
        --------
        # >>> strategy.trades = [
        # ...     Trade(close_bar='Bar0', asset=['Asset0', 'Asset1'], ...),
        # ...     Trade(close_bar='Bar1', asset=['Asset2'], ...),
        # ... ]
        # >>> History()._get_close_bar(strategy)
        # array([  'Bar0'  'Bar0'  'Bar1'])
        """
        return np.repeat(
            [trade.close_bar for trade in strategy.trades],
            [trade.n_orders for trade in strategy.trades],
        )

    @staticmethod
    def _get_shut_bar(strategy):
        """
        Return shut_bar of each order.

        Returns
        -------
        array_shut_bar : array, shape (n_orders, )

        Examples
        --------
        # >>> strategy.trades = [
        # ...     Trade(shut_bar='Bar0', asset=['Asset0', 'Asset1'], ...),
        # ...     Trade(shut_bar='Bar1', asset=['Asset2'], ...),
        # ... ]
        # >>> History()._get_shut_bar(strategy)
        # array([  'Bar0'  'Bar0'  'Bar1'])
        """
        return np.repeat(
            [trade.shut_bar for trade in strategy.trades],
            [trade.n_orders for trade in strategy.trades],
        )

    @staticmethod
    def _get_take(strategy):
        """
        Return take of each order.

        Returns
        -------
        array_take : numpy.array, shape (n_orders, )

        Examples
        --------
        # >>> strategy.trades
        # ... [
        # ...     Trade(take=1, asset=['Asset0', 'Asset1'], ...),
        # ...     Trade(take=2, asset=['Asset2'], ...),
        # ... ]
        # >>> History()._get_take
        # array([  1  1  2])
        """
        return np.repeat(
            [trade.take for trade in strategy.trades],
            [trade.n_orders for trade in strategy.trades],
        )

    @staticmethod
    def _get_stop(strategy):
        """
        Return stop of each order.

        Returns
        -------
        array_stop : numpy.array, shape (n_orders, )

        Examples
        --------
        # >>> strategy.trades = [
        # ...     Trade(stop=-1, asset=['Asset0', 'Asset1'], ...),
        # ...     Trade(stop=-2, asset=['Asset2'], ...),
        # ... ]
        # >>> strategy.stop
        # array([ -1 -1 -2])
        """
        return np.repeat(
            [trade.stop for trade in strategy.trades],
            [trade.n_orders for trade in strategy.trades],
        )

    @staticmethod
    def _get_pnl(strategy):
        return np.concatenate(
            [trade.final_pnl(strategy.universe) for trade in strategy.trades]
        )
