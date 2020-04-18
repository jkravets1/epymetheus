class NoTradeError(RuntimeError):
    """
    Exception class to raise if no trades are yielded.
    """


class NotRunError(ValueError):
    """
    Exception class to raise if strategy is not run.
    """
