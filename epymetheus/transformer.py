# from sklearn.base import TransformerMixin
# import numpy as np


# class Cross(TransformerMixin):

#     def __init__(self):
#         pass

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X, y=None):
#         """
#         Parameters
#         ----------
#         - X : array-like, shape (n_samples, n_features)

#         Returns
#         -------
#         - X_signal : array-like, shape (n_samples, n_features)

#         Examples
#         --------
#         >>> X
#         array([[-1, -1],
#                [ 1,  0],
#                [ 2,  1],
#                [ 1,  0],
#                [-2, -1]])
#         >>> Cross().transform(X)
#         array([[ 0,  0],
#                [ 1,  0],
#                [ 0,  1],
#                [ 0,  0],
#                [-1, -1]])
#         """
#         out = np.sign(np.diff(np.sign(X), axis=0)) * (X[1:, :] != 0)
#         zeros = np.zeros(np.shape(X)[1], dtype=np.int8).reshape(1, -1)
#         return np.vstack([zeros, out])


# class SignalToTrades:
#     """
#     Yield `Trade` from signal.

#     Parameters
#     ----------
#     - signal_close_long : float, default -inf
#         The signal to close an existing long-position.
#     - signal_close_short : float, default inf
#         The signal to close an existing short-position.
#     - long_after_long : {'ignore', 'add', 'replace'}
#         How to deal with the long-signal when opening a long position.
#         If 'ignore':
#             just ignore the long-signal.
#         If 'add':
#             open a new position keeping the existing position untouched.
#         If 'replace':
#             close the existing position and open a new position.
#     - short_after_long : {'ignore', 'add', 'replace', 'cut'}
#         How to deal with the long-signal when opening a long position.
#         If 'ignore':
#             just ignore the long-signal.
#         If 'add':
#             open a new position, keeping the existing position untouched.
#         If 'replace':
#             close the existing position and open a new position.
#         If 'cut':
#             ...
#     - short_after_short :{'ignore', 'add', 'replace'}
#         How to deal with the short-signal when opening a short position.
#     - long_after_short : {'ignore', 'add', 'replace', 'cut'}
#         How to deal with the long-signal when opening a short position.

#     Yields
#     ------
#     Trade
#     """
#     def __init__(self):
#         pass

#     # TODO halfway

#     # def yields(self, X):
#     #     """
#     #     Parameters
#     #     ----------
#     #     - X : array-like, shape (n_samples, n_features)
#     #         1 means signal to open, -1 means close
#     #     """
#     #     for x in X:  # column
#     #         signal_open = compress(range(x.shape[0]), x == 1)
#     #         signal_close_long \
#     #             = compress(range(x.shape[0]), x == self.signal_close_long)
#     #         signal_close_short \
#     #             = compress(range(x.shape[0]), x == self.signal_close_short)

#     #         # TODO XXX

#     #         now = next(opens, -1)  # -1 is sentinel
#     #         opening = False

#     #         timing = []
#     #         while True:
#     #             if opening:
#     #                 next_ = next(close, -1)
#     #                 if next_ > now:
#     #                     timing.append((now, next_))
#     #                     now = next_
#     #                     opening = False
#     #             else:
#     #                 next_ = next(opens, -1)
#     #                 if next_ > now:
#     #                     now = next_
#     #                     opening = True

#     #             if date_next == -1:
#     #                 return timing


# class IterativeTransformer():

#     def __init__(self, transformer):
#         self.transformer = transformer

#     def transform(self, X, **kwargs):
#         """
#         Parameters
#         ----------
#         """
#         def row(i_row):
#             # if i_row == 0:  # not necessary?
#             #     return np.full((1, X.shape[1]), np.nan)
#             return self.transformer.transform(
#                 X[:i_row, :], **kwargs
#             ).reshape(1, -1)

#         return np.vstack([
#             row(i_row) for i_row in range(X.shape[0])
#         ])


# class Barrier(TransformerMixin):
#     pass  # TODO
