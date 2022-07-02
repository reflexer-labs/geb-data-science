# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of the easydev software
#
#  Copyright (c) 2012-2014 -
#
#  File author(s): Thomas Cokelaer (cokelaer, gmail.com)
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: https://github.com/cokelaer/easydev
#  website: http://github.com/cokelaer/easydev
#
##############################################################################
"""Handy decorators"""
from functools import wraps
import threading

__all__ = ["ifpylab", "requires", "ifpandas"]


# decorator with arguments and optional arguments for a method
def _require(*args_deco, **kwds_deco):
    """Decorator for class method to check if an attribute exist

    .. doctest::

        from easydev.decorators import require

        class Test(object):
            def __init__(self):
               self.m = 1
            @require('m', "set the m attribute first")
            def print(self):
                print self.m
        t = Test()
        t.print()


    .. todo:: first argument could be a list
    """
    if len(args_deco) != 2:
        raise ValueError(
            "require decorator expects 2 parameter. First one is"
            + "the required attribute. Second one is an error message."
        )
    attribute = args_deco[0]
    msg = args_deco[1]

    if len(attribute.split(".")) > 2:
        raise AttributeError(
            "This version of require decorator introspect only 2 levels"
        )

    def decorator(func):
        # func: function object of decorated method; has
        # useful info like f.func_name for the name of
        # the decorated method.

        def newf(*args, **kwds):
            # This code will be executed in lieu of the
            # method you've decorated.  You can call the
            # decorated method via f(_args, _kwds).
            names = attribute.split(".")

            if len(names) == 1:
                if hasattr(args[0], attribute):
                    return func(*args, **kwds)
                else:
                    raise AttributeError("%s not found. %s" % (names, msg))
            elif len(names) == 2:
                if hasattr(getattr(args[0], names[0]), names[1]):
                    return func(*args, **kwds)
                else:
                    raise AttributeError("%s not found. %s" % (names, msg))

        newf.__name__ = func.__name__
        newf.__doc__ = func.__doc__
        return newf

    return decorator


# for book keeping, could be useful:
"""
def _blocking(not_avail):
    def blocking(f, *args, **kw):
        if not hasattr(f, "thread"):
            # no thread running
            def set_result():
                f.result = f(*args, **kw)
            f.thread = threading.Thread(None, set_result)
            f.thread.start()
            return not_avail
        elif f.thread.isAlive():
            return not_avail
        else:
            # the thread is ended, return the stored result
            del f.thread
            return f.result
    return blocking
"""

# same as require decorator but works with list of stirngs of
# single string and uses the functools utilities
def requires(requires, msg=""):
    """Decorator for class method to check if an attribute exist

    .. doctest::

        >>> from easydev.decorators import requires
        >>> class Test(object):
        ...     def __init__(self):
        ...         self.m = 1
        ...         self.x = 1
        ...     @requires(['m','x'], "set the m attribute first")
        ...     def printthis(self):
        ...         print(self.m+self.x)
        >>> t = Test()
        >>> t.printthis()
        2

    """
    if isinstance(requires, str):
        requires = [requires]
    elif isinstance(requires, list) == False:
        raise TypeError(
            "First argument of the /requires/ decorator must be a"
            + "string or list of string representing the required attributes"
            + "to be found in your class. Second argument is a "
            + "complementary message. "
        )

    def actualDecorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            for require in requires:
                if hasattr(args[0], require) == False:
                    raise AttributeError(
                        "{} not found in {}. ".format(require, args[0]) + msg
                    )
            return f(*args, **kwds)

        return wrapper

    return actualDecorator


# could be a macro maybe


def ifpandas(func):
    """check if pandas is available. If so, just return
    the function, otherwise returns dumming function
    that does nothing

    """

    def wrapper(*args, **kwds):
        return func(*args, **kwds)

    try:
        import pandas

        return wrapper
    except Exception:  # pragma: no cover

        def dummy():
            pass

        return dummy


def ifpylab(func):
    """check if pylab is available. If so, just return
    the function, otherwise returns dumming function
    that does nothing
    """
    # for functions
    def wrapper(*args, **kwds):
        return func(*args, **kwds)

    # for methods
    try:
        import pylab

        return wrapper
    except Exception:  # pragma: no cover

        def dummy():
            pass

        return dummy
