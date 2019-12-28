class TradeBacktester:

    def __init__(
        self,
        begin_date=None,
        end_date=None,
        init_wealth=None,
        commission_model=None,
        slippage_model=None,
    ):
        """Initialize self."""
        self.begin_date = begin_date
        self.end_date = end_date
        # not implemented below
        self.init_wealth = init_wealth
        self.commission_model = commission_model
        self.slippage_model = slippage_model

    def run(
        self,
        trade_strategy: TradeStrategy,  # and AllocationStrategy
        universe: Universe,
    ):
        """
        Run backtest.

        Parameters
        ----------
        - initial_wealth : int or float, default None
            Wealth before investing.
            If None, results that need it will not be evaluated.
        - universe : Universe
            Universe to run a backtesting with.
        - path : str, path object or file-like object, default ``self.name``
            Directory to export the result.
            If ``path`` does not yet exist, it is created.
            While ``path`` already exists, overwriting is avoided by
            ``path = path + '_'``.

        Outputs
        -------
        cf. TradeResult.export
        - 'summary.md' : Summary of backtesting.
        - 'trades.csv' : Csv of trades.
        - 'wealth.csv' : Csv of historical cumulative wealth.
        - 'record.csv' : Csv of return of each trade.
        - 'wealth.png' : Line graph of historical cumulative wealth.
        - 'record.png' : Histogram of return of each trade.

        They will be exported as ``path/summary.md`` etc.

        Returns
        -------
        TradeResult

        Examples
        --------
        >>> runner = Runner()
        >>> runner.run()  # like fit of sklearn
        >>> result = runner.result
        """
        self.__result = TradeResult(runner=self, strategy=trade_strategy, universe=universe)
        return self.result

    def run_export(self, trade_strategy, universe):
        self.run(trade_strategy=trade_strategy, universe=universe)
        result.export()
        return self.result

    @property
    def result(self):
        return self.__result


class TradeResult:

    def __init__(self, runner, trade_strategy, universe):
        pass

    @property
    def wealth(self):
        pass

    @property
    def gains(self):
        pass

    @property
    def durations(self):
        pass

    def summary(self, style='md'):
        if style == 'md':
            return self.__summary_md()
        if style == 'std':
            return self.__summary_std()
        raise ValueError(f'Invalid style: {style}')

    def export_summary(self, path):
        suffix = pathlib.Path(path).suffix.lstrip('.')
        if suffix in ('md', 'txt'):
            with open(path, 'w') as f:
                summary = self.summary(style='md')
                f.write(summary)
        if suffix in ('pdf'):
            raise NotImplementedError  # md -> pdf
        raise ValueError(f'Invalid suffix of path: {path}')


def max_drop(trade_result):
    pass

# etc
