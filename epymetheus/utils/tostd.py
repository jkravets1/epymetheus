# import pandas as pd


# def underline(s: str, style: str = '-'):
#     return '{}\n{}\n'.format(s, style * len(s))


# def itemize(items):
#     if isinstance(items, list):
#         return ''.join([
#             '- {}\n'.format(item) for item in items
#         ])
#     if isinstance(items, dict):
#         len_key = max(map(len, items.keys()))
#         return ''.join([
#             '- {} : {}\n'.format(key.ljust(len_key), value)
#             for key, value in items.items()
#         ])
#     raise TypeError


# def table(dataframe: pd.DataFrame):
#     return str(dataframe)
