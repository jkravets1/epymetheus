# from pytablewriter import MarkdownTableWriter as tablewriter


# def section(s: str, level: int = 1):
#     return '{} {}\n'.format('#' * level, s)


# def itemize(items):
#     if isinstance(items, list):
#         return ''.join([
#             '- {}\n'.format(item) for item in items
#         ])
#     if isinstance(items, dict):
#         return ''.join([
#             '- **{}** : {}\n'.format(key, value)
#             for key, value in items.items()
#         ])
#     raise TypeError


# def figure(src, alt='', title=''):
#     return '![{}]({} "{}")'.format(alt, src, title)


# def table(dataframe):
#     table = tablewriter()
#     table.from_dataframe(dataframe, add_index_column=True)
#     return table.dumps()
