from functools import wraps

def require_attributes(param, attrs):
    """
    Raise ValueError if param does not have attrs.

    Examples
    --------
    >>> @require_attributes('param', ['attr0', 'attr1'])
    >>> def function(param):
    >>>     return param.attr0 + attr1
    >>>
    >>> param = ...
    """

    def _check(func):

        def f(*args, **kwargs):
            for attr in attrs:
                if not hasattr(eval(param), attr):
                    raise ValueError(f'{func.__name__} requres {param}.{attr}')
            return func(*args, **kwargs)

        return f

    return _check
