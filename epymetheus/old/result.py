# flake8: noqa


class TradeResult():
    """
    Represent backtest result of ``TradeStrategy``.
    Parameters
    ----------
    - strategy : TradeStrategy
        ``TradeStrategy`` to run backtesting.
    - universe : Universe
        ``Universe`` to run backtesting with.
    Attributes
    ----------
    - strategy : TradeStrategy
        Used ``TradeStrategy``.
    - universe : Universe
        Used ``Universe``.
    - trades : list of Trade
        Cumulative gain and loss.
    - record : pandas.Series
        Cumulative gain and loss of each trade.
    - wealth : pandas.Series
        Cumulative gain and loss.
    - overview : dict
    - tradestat : dict
    - winlose : dict
    - backtest_time : datetime.timedelta
    """
    def __init__(
        self,
        strategy: TradeStrategy,
        universe: Universe,
        # initial_wealth:float = None,  # TODO
        # commission_rate:float = 0,  # TODO
    ):
        time_start = time.time()

        print('Generating trades ...')
        list_trade = list(strategy.logic(universe, **strategy.parameters))
        position = Position.from_trades(list_trade, universe)

        print('Evaluating statistics ...')
        wealth = position.wealth(universe)

        _array_duration = np.array(
            [trade.duration.days for trade in list_trade]
        )

        array_gain = np.array([trade.gain(universe) for trade in list_trade])
        _array_gain_win = array_gain[array_gain > .0]
        _array_gain_lose = array_gain[array_gain <= .0]

        ndigits = 5

        self._strategy = strategy
        self._universe = universe
        self._list_trade = list_trade

        self._wealth = wealth
        self._record = pd.Series(array_gain)
        self._net_exposure = position.net_exposure(universe)
        self._abs_exposure = position.abs_exposure(universe)
        self._volume = position.volume(universe)

        self._overview = {
            'fin wealth':       round(wealth[-1], ndigits),
            'max drop':         round(wealth.drop().min(), ndigits),
            'avg gain':         round(np.nanmean(array_gain), ndigits),
            'med gain':         round(np.nanmedian(array_gain), ndigits),
        }
        self._tradestat = {
            'num trade':        len(list_trade),
            'avg duration':     str(int(np.nanmean(_array_duration))) + ' days',
            'med duration':     str(int(np.nanmedian(_array_duration))) + ' days',
            'max duration':     str(int(np.max(_array_duration))) + ' days',
            'min duration':     str(int(np.min(_array_duration))) + ' days',
        }
        # TODO max/min yield error if array is empty
        self._winlose = {
            'num win':          len(_array_gain_win),
            'num lose':         len(_array_gain_lose),
            'avg gain win':     round(np.nanmean(_array_gain_win), ndigits),
            'med gain win':     round(np.median(_array_gain_win), ndigits),
            'max gain win':     round(np.max(_array_gain_win), ndigits),
            'min gain win':     round(np.min(_array_gain_win), ndigits),
            'avg gain lose':    round(np.nanmean(_array_gain_lose), ndigits),
            'med gain lose':    round(np.nanmedian(_array_gain_lose), ndigits),
            'max gain lose':    round(np.max(_array_gain_lose), ndigits),
            'min gain lose':    round(np.min(_array_gain_lose), ndigits),
        }

        self._runtime = time.time() - time_start

    @property
    def strategy(self):
        """Return used ``TradeStrategy``. """
        return self._strategy

    @property
    def universe(self):
        """Return used ``Universe``. """
        return self._universe

    @property
    def list_trade(self):
        """Return list of ``Trade``."""
        return self._list_trade

    @property
    def wealth(self):
        """Return cumulative wealth as pd.Series."""
        return self._wealth

    @property
    def record(self):
        """Return final gain of each trade as pd.Series."""
        return self._record

    @property
    def net_exposure(self):
        """Return net exposure as pd.Series."""
        return self._net_exposure

    @property
    def abs_exposure(self):
        """Return net exposure as pd.Series."""
        return self._abs_exposure

    @property
    def volume(self):
        """Return time-series of transaction volumes."""
        return self._volume

    @property
    def overview(self):
        """
        Return overview of result as ``dict``.
        Keys
        ----
        - 'fin wealth'
        - 'max drop'
        - '[avg|med] gain'
        """
        return self._overview

    @property
    def tradestat(self):
        """
        Return trade statistics in ``dict``.
        Keys
        ----
        - 'num trade' : int
        - '[avg|med|max|min] duration' : datetime.timedelta
        """
        return self._tradestat

    @property
    def winlose(self):
        """
        Return statistics of win/lose trades in ``dict``.
        Keys
        ----
        - 'num [win|lose]'
        - '[avg|med|max|min] gain [win|lose]'
        """
        return self._winlose

    @property
    def runtime(self):
        """Time took to run backtesting as ``datetime.timedelta``."""
        return self._runtime

    def summary(
        self,
        style,
        path_fig_wealth=None,
        path_fig_record=None
    ):
        """
        Returns summary of the result as ``str``.
        Parameters
        ----------
        - style : {'std', 'md'}
        """
        def _summary_std(self):
            s = '\n'
            s += to_std.underline(self.strategy.name, style='=')
            s += self.strategy.description + '\n\n'

            _dict_universe = {
                'Universe': self.universe.name,
                'Period': '{} - {} ({})'.format(
                    self.universe.begin_date.strftime('%Y/%m/%d'),
                    self.universe.end_date.strftime('%Y/%m/%d'),
                    str(self.universe.duration.days) + ' days',
                )
            }
            s += to_std.underline('Parameters used')
            s += to_std.itemize(self.strategy.parameters) + '\n'

            s += to_std.underline('Universe')
            s += to_std.itemize(_dict_universe) + '\n'

            s += to_std.underline('Overview')
            s += to_std.itemize(self.overview) + '\n'

            s += to_std.underline('Trade statistics')
            s += to_std.itemize(self.tradestat) + '\n'

            items = ('num', 'avg gain', 'med gain', 'max gain', 'min gain')
            s += to_std.underline('Win and lose')
            s += to_std.table(pd.DataFrame({
                winlose: [self.winlose['{} {}'.format(item, winlose)]
                          for item in items]
                for winlose in ('win', 'lose')
            }, index=items)) + '\n'

            s += '\n*** Runtime : {} sec ***\n'.format(round(self.runtime, 1))
            return s

        def _summary_md(self, path_fig_wealth, path_fig_record):
            s = to_md.section(self.strategy.name, level=1)
            s += self.strategy.description + '\n\n'

            _dict_universe = {
                'Universe': self.universe.name,
                'Period': '{} - {} ({})'.format(
                    self.universe.begin_date.strftime('%Y/%m/%d'),
                    self.universe.end_date.strftime('%Y/%m/%d'),
                    str(self.universe.duration.days) + ' days',
                )
            }
            s += to_md.section('Parameters used', level=2)
            s += to_md.itemize(self.strategy.parameters) + '\n'
            s += to_md.section('Universe', level=2)
            s += to_md.itemize(_dict_universe)

            s += '\n|{}|{}|\n|:-:|:-:|\n|{}|{}|\n'.format(
                'wealth and exposure', 'record',
                to_md.figure(path_fig_wealth, alt='wealth'),
                to_md.figure(path_fig_record, alt='record'),
            ) + '\n'

            s += to_md.section('Overview', level=2)
            s += to_md.itemize(self.overview) + '\n'
            s += to_md.section('Trade statistics', level=2)
            s += to_md.itemize(self.tradestat) + '\n'

            items = ('num', 'avg gain', 'med gain', 'max gain', 'min gain')
            s += to_md.section('Win and lose', level=2)
            s += to_md.table(pd.DataFrame({
                winlose: [self.winlose['{} {}'.format(item, winlose)]
                          for item in items]
                for winlose in ('win', 'lose')
            }, index=items)) + '\n'

            s += 'Backtest runtime : {} sec'.format(round(self.runtime, 1))

            return s

        if style == 'std':
            return _summary_std(self)
        elif style == 'md':
            return _summary_md(self, path_fig_wealth, path_fig_record)
        else:
            raise ValueError(
                'Style must be std or md, but given {}'.format(style)
            )

    def export(self, path):

        def plot_record(record, path, bins=100):
            """Export histogram of records to path."""
            plt.figure(figsize=(8, 8))
            plt.hist(record, bins=bins)
            plt.axvline(x=0, color='k', linestyle='--')
            plt.title('record')
            plt.savefig(path)
            plt.close('all')

        def plot_wealth_exposure(wealth, net_exposure,
                                 abs_exposure, volume, path):
            """Export [net|abs]_exposure and volume."""
            ratio = 2  # height of wealth : exposure = ratio : 1
            fig = plt.figure(figsize=(8, 8))
            grid = gridspec.GridSpec(ratio + 1, 1)
            ax1 = fig.add_subplot(grid[:ratio, 0], title='wealth')
            ax2 = fig.add_subplot(grid[-1, 0], title='exposure', sharex=ax1)

            ax1.plot(wealth)
            ax1.axhline(y=0, color='k', linestyle='--')

            ax2.plot(volume, label='volume')
            ax2.plot(abs_exposure, label='abs exposure')
            ax2.plot(net_exposure, label='net exposure')
            ax2.legend()
            plt.setp(ax1.get_xticklabels(), visible=False)

            plt.savefig(path)
            plt.close('all')

        path = p = pathlib.Path(path)
        i = 1
        while p.exists():
            p = path.with_name('{} ({})'.format(path.stem, i))
            i += 1
        path = p
        path.mkdir(parents=True)

        print('Exporting result ...')
        path_md_summary = path / 'summary.md'
        path_csv_wealth = path / 'wealth.csv'
        path_csv_record = path / 'record.csv'
        path_csv_trades = path / 'trades.csv'
        path_csv_volume = path / 'volume.csv'
        path_fig_wealth = path / 'wealth.png'
        path_fig_record = path / 'record.png'
        path_csv_net_exposure = path / 'net_exposure.csv'
        path_csv_abs_exposure = path / 'abs_exposure.csv'

        df_quote = pd.concat([
            trade._to_dataframe(trade_index=i)
            for i, trade in enumerate(self.list_trade)
        ], ignore_index=True)
        df_quote.to_csv(path_csv_trades)

        self.wealth.to_csv(path_csv_wealth, header=False)
        self.record.to_csv(path_csv_record, header=False)
        self.volume.to_csv(path_csv_volume, header=False)
        self.net_exposure.to_csv(path_csv_net_exposure, header=False)
        self.abs_exposure.to_csv(path_csv_abs_exposure, header=False)

        plot_wealth_exposure(self.wealth, self.net_exposure,
                             self.abs_exposure, self.volume,
                             path_fig_wealth)
        plot_record(self.record, path_fig_record)

        with open(path_md_summary, mode='w') as f:
            summary = self.summary(
                style='md',
                path_fig_wealth=path_fig_wealth.name,
                path_fig_record=path_fig_record.name,  # TODO dirty
            )
            f.write(summary)

        print(self.summary(style='std'))

        print('Result was exported to: {}'.format(path))
