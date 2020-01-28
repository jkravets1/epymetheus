# import pandas_datareader
# import pandas as pd
# import datetime

# from epymetheus.core.api import Asset


# DEFAULT_BEGIN_DATE = datetime.date(1900, 1, 1)
# DEFAULT_END_DATE = pd.Timestamp.today()


# def read_web(
#     asset: Asset,
#     source: str,
#     column: str,
#     scraper_ticker=None,
#     begin_date=None,
#     end_date=None,
# ):
#     """
#     Parameters
#     ----------
#     - asset : Asset
#         The asset to fetch the data.
#     - source : str
#         The website from which the data is fetched.
#     - column : str
#         The column to leave.  e.g.) 'Adj Close'.
#     - scraper_ticker : str, default ``asset.ticker``
#         The ticker which is passed to pandas_datareader.
#     - begin_date: datetime.date, default ``1990-01-01``
#         The begin date to fetch data.
#     - end_date: datetime.date, default today
#         The end date to fetch data.
#     Examples
#     --------
#     >>> asset = epymetheus.Asset(ticker='VTI')
#     >>> epymetheus.read_web(
#     ...     asset,
#     ...     source='yahoo',
#     ...     column='Adj Close',
#     ...     begin_date=bd,
#     ...     end_date=bd,
#     ...     )
#     """
#     scraper_ticker = scraper_ticker or asset.ticker
#     begin_date = begin_date or DEFAULT_BEGIN_DATE
#     end_date = end_date or DEFAULT_END_DATE

#     try:
#         df = pandas_datareader.data.DataReader(
#             name=scraper_ticker,
#             data_source=source,
#             start=begin_date,
#             end=end_date,
#         ).loc[:, [column]]
#         df.rename(columns={column: asset.ticker}, inplace=True)
#     except (pandas_datareader._utils.RemoteDataError,
#             NotImplementedError,
#             KeyError,
#             ValueError,
#             ) as e:
#         print('Error with', asset)
#         raise e
#     else:
#         df.index.name = 'Date'
#         return df


# def renew_asset(
#     asset: Asset,
#     source: str,
#     column: str,
#     scraper_ticker=None,
# ):
#     """
#     Renews the local data by fetching the data from the web.
#     Parameters
#     ----------
#     - asset : Asset
#         The asset to renew the data.
#     - source : str
#         The website from which the data is fetched.
#     - column : str
#         The column to leave.
#     - scraper_ticker : str, default ``asset.ticker``
#         The ticker which is passed to pandas_datareader.
#     """
#     scraper_ticker = scraper_ticker or asset.ticker

#     error = True
#     try:
#         df_old = asset.read()
#     except FileNotFoundError:  # TODO use Path.exists instead
#         df_old = pd.DataFrame({asset.ticker: []}, index=[])
#         df_old.index.name = 'Date'
#         begin_date = DEFAULT_BEGIN_DATE
#         error = False
#     else:
#         begin_date = df_old.index[-1] + datetime.timedelta(days=1)
#         error = False

#     end_date = DEFAULT_END_DATE

#     if not error:
#         if begin_date < end_date:
#             try:
#                 df_add = read_web(
#                     asset=asset,
#                     source=source,
#                     column=column,
#                     scraper_ticker=scraper_ticker,
#                     begin_date=begin_date,
#                     end_date=end_date,
#                 )
#             except ValueError as e:
#                 print('Error occured with', asset)
#                 raise e
#             else:
#                 df_new = pd.concat([df_old, df_add])

#                 # Remove duplicate
#                 i = df_new.index[df_new.index.duplicated(keep='first')]
#                 df_new.drop(i, inplace=True)

#                 # Fill holidays with the data of the last weekdays
#                 df_new = df_new.asfreq('1D', method='ffill')
#                 df_new.fillna(method='ffill', inplace=True)

#                 df_new.to_csv(asset.path)
