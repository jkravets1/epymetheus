import pytest

import pandas as pd

from epymetheus import Trade, Universe, Strategy
from epymetheus.benchmarks import DeterminedTrader
from epymetheus.datasets import make_randomwalk
from epymetheus.exceptions import NoTradeError


trade0 = Trade(
    asset=["Asset0", "Asset1"],
    lot=[1, 2],
    open_bar="Bar0",
    shut_bar="Bar1",
    take=3,
    stop=4,
)
trade1 = Trade(
    asset=["Asset2", "Asset3"],
    lot=[5, 6],
    open_bar="Bar2",
    shut_bar="Bar3",
    take=7,
    stop=8,
)

trades = [trade0, trade1]

universe = Universe(
    prices=pd.DataFrame(
        {f"A{i}": range(10) for i in range(10)}, index=[f"B{i}" for i in range(10)]
    )
)


params_trades = [trades]
params_universe = [universe]
params_verbose = [True, False]


class HardCodedStrategy(Strategy):
    """
    Yield hard-coded trades.
    """

    def __init__(self):
        self.trade0 = Trade(
            asset="A0", lot=1.0, open_bar="B0", shut_bar="B1", take=2.0, stop=-2.0
        )
        self.trade1 = Trade(
            asset="A1", lot=1.1, open_bar="B2", shut_bar="B3", take=2.1, stop=-2.1
        )

    def logic(self, universe):
        yield self.trade0
        yield self.trade1


class NoTradeStrategy(Strategy):
    """
    Yields no strategy. Used in `TestRun.test_no_trade_error`.
    """

    def logic(self, universe):
        pass


# --------------------------------------------------------------------------------


class TestRun:
    """
    Test `Strategy.run()`.
    """

    params_verbose = [True, False]

    @pytest.mark.parametrize("verbose", params_verbose)
    def test_generate(self, verbose):
        strategy = HardCodedStrategy()
        strategy.run(universe, verbose=verbose)
        expected = [strategy.trade0, strategy.trade1]

        assert strategy.trades == expected

    @pytest.mark.parametrize("verbose", params_verbose)
    def test_no_trade_error(self, verbose):
        strategy = NoTradeStrategy()
        with pytest.raises(NoTradeError):
            strategy.run(make_randomwalk(seed=42), verbose=verbose)


class TestExecute:
    """
    Test `Strategy.execute()`.
    """

    @pytest.mark.parametrize("trades", [trades])
    @pytest.mark.parametrize("universe", [universe])
    @pytest.mark.parametrize("verbose", params_verbose)
    def test_execute(self, trades, universe, verbose):
        strategy = DeterminedTrader(trades=trades)
        strategy.run(universe, verbose=verbose)

        close_bar_expected = [
            trade.execute(universe).close_bar for trade in strategy.trades
        ]
        pnl_expected = [trade.execute(universe).pnl for trade in strategy.trades]

        assert [trade.close_bar for trade in strategy.trades] == close_bar_expected
        assert [trade.pnl for trade in strategy.trades] == pnl_expected

    def test_result(self):
        pass  # TODO: is close_bar as expected?
