import numpy as np

from sklearn.linear_model import LinearRegression


class ThreeFactorAnalizer:
    """
    Parameters
    ----------
    market : pandas.Series
        Market, price base
    smb : pandas.Series
        Size: small - big, price base
    hml : pandas.Series
        Value: high - low, price base
    r : float, default 0.0
        Risk-free rate.
    freq : DateOffset
    Attributes
    ----------
    alpha_ : array of shape (n_samples, ) or (n_targets, n_samples)
        Excess return
    coef_ : array of shape (3, ) or (n_targets, 3)
    """
    def __init__(self, mkt, smb, hml, rf=.0, freq='1D'):
        """Initialize self."""
        self.rf = rf
        self.mkt = mkt
        self.smb = smb
        self.hml = hml
        self.freq = freq
        # TODO nan policy

    def fit(self, price):
        # TODO begin and end date
        # TODO freq
        lin_reg = LinearRegression()
        X = np.array([
            self.mkt.pct_change(),
            self.smb.pct_change(),
            self.hml.pct_change(),
        ])
        y = price.pct_change()

        lin_reg.fit(X, y)

        self.coef_ = lin_reg.coef_
        self.alpha_ = y - lin_reg.predict(X)

    def transform(self, price, asframe=False):
        if asframe:
            pass  # return as pd.Series / pd.DataFrame
        return (1 + self.alpha_).cumprod()
