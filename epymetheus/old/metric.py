# flake8: noqa


class Wealth(pd.Series):
    """
    Represent time-series of wealth.
    Inheriting ``pd.Series``.
    """
    def __init__(
        self,
        data=None,
        index=None,
        **kwargs,
    ):
        """Initialize self."""
        # check if index is datetime.date
        super(Wealth, self).__init__(
            data=data,
            index=index,
            **kwargs,
        )

    @property
    def begin_date(self):
        """Return begin date of investment."""
        return self.index[0]

    @property
    def end_date(self):
        """Return end date of investment."""
        return self.index[-1]

    @property
    def duration(self):
        """Return duration of investment."""
        return self.index[-1] - self.index[0]

    def initial_wealth(self):
        """Return wealth on the first date."""
        return self.iat[0]

    def final_wealth(self):
        """Return wealth on the last date."""
        return self.iat[-1]

    def annual_return(self):
        """Return annual compound return."""
        r = self.final_wealth / self.initial_wealth
        y = self.duration.days / DAY_PER_YEAR
        return np.exp(np.log(1 + r) / y) - 1

    def annual_volatility(
        self,
        ignore_holidays=False,
        ignore_upside=False,
    ):
        """Return annual standard deviation of return."""
        dpy = WEEKDAY_PER_YEAR if ignore_holidays else DAY_PER_YEAR
        if ignore_upside:
            return np.std(np.clip(self.pct_change(), 0, None)) * np.sqrt(dpy)
        else:
            return np.std(self.pct_change()) * np.sqrt(dpy)

    def drop(self):
        """Return time-series of drop from cumulative max in pd.Series."""
        return self - self.cummax()

    def drawdown(self):
        """Return time-series of drawdown rate in pd.Series."""
        return 1 - self / self.cummax()

    def sharpe_ratio(
        self,
        ignore_holidays=False,
        risk_free_return=0.0  # ann return of risk free asset.
    ):
        """Return Sharpe ratio of self."""
        return (self.annual_return - risk_free_return) \
            / self.annual_volatility(
                ignore_holidays=ignore_holidays,
                ignore_upside=False
            )

    def sortino_ratio(
        self,
        ignore_holidays=False,
        risk_free_return=0.0
    ):
        """Return Sortino ratio of self."""
        return (self.annual_return - risk_free_return) \
            / self.annual_volatility(ignore_holidays=ignore_holidays,
                                     ignore_upside=True)

    def traynor_ratio(
        self,
        benchmark: pd.Series,
        ignore_holidays=False,
        risk_free_return=0.0,
    ):
        """Return Traynor ratio of self."""
        return (self.annual_return - risk_free_return) \
            / self.beta(benchmark)

    def information_ratio(
        self,
        benchmark: pd.Series,
        ignore_holidays=False,
        by='std',
    ):
        # TODO slice benchmark to make index same
        return self.alpha(benchmark) / \
            self.tracking_error(
                benchmark,
                ignore_holidays=ignore_holidays,
                by=by
            )

    def alpha(self, benchmark: pd.Series):
        """Returns annual alpha against benchmark."""
        # TODO slice benchmark to make index equal
        benchmark_wealth = Wealth(benchmark)
        if self.duration != benchmark_wealth.duration:
            raise ValueError
        return self.annual_return - benchmark_wealth.annual_return

    def beta(self, benchmark: pd.Series):
        """Returns annual beta against benchmark."""
        # TODO slice benchmark to make index same
        return np.cov(self, benchmark) / np.var(benchmark)

    def tracking_error(
        self,
        benchmark: pd.Series,
        ignore_holidays=False,
        by='std',
    ):
        """
        Returns annual tracking error.
        Parameters
        ----------
        - benchmark : pd.Series
        - ignore_holidays : bool
        - by : {'std', 'rms'}
            If 'std', return standard deviation of difference of returns.
            If 'rms', return root-mean-square of difference of returns.
        """
        # TODO slice benchmark to make index same
        # TODO unbiased
        dpy = WEEKDAY_PER_YEAR if ignore_holidays else DAY_PER_YEAR
        if by == 'std':
            return np.std(
                self.pct_change() - benchmark.pct_change()
            ) * np.sqrt(dpy)
        if by == 'rms':
            return np.linarg.norm(
                self.pct_change() - benchmark.pct_change()
            ) / (self.duration.days / dpy)
        raise ValueError(
            "Given value of 'by' {} is not in {'std', 'rms'}.".format(by)
        )

    def value_at_risk(self):
        pass  # TODO
