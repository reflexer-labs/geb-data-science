# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of the easydev software
#
#  Copyright (c) 2011-2014
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: https://github.com/cokelaer/easydev
#  Documentation: http://packages.python.org/easydev
#
##############################################################################
# $:Id $

import tempfile

__all__ = ["assert_list_almost_equal", "trysetattr", "TempFile"]

# from easydev.decorators import ifpandas


def assert_list_almost_equal(first, second, places=None, deltas=None):
    """Combined version nose.tools.assert_almost_equal and assert_list_equal

    This function checks that 2 lists contain identical items.
    The equality between pair of items is checked with assert_almost_equal
    function, which means you can check for the places argument

    .. note:: there may be already some tools to
        check that either in nosetests or unittest
        but could not find.

    .. doctest::

        >>> from easydev.easytest import assert_list_almost_equal
        >>> assert_list_almost_equal([0,0,1], [0,0,0.9999], places=3)
        >>> assert_list_almost_equal([0,0,1], [0,0,0.9999], deltas=1e-4)

    """
    if places:
        deltas = 10 ** -(places - 1)

    if deltas:
        for x, y in zip(first, second):
            if abs(x - y) > deltas:
                raise ValueError


def trysetattr(this, attrname, value, possible):
    """A common test pattern: try to set a non-writable attribute

    ::

        class A(object):
            def __init__(self):
                self._a = 1
                self._b = 2
            def _get_a(self):
                return self._a
            def _set_a(self, value):
                self._a = value
            a = property(_get_a, _get_b)
            def _get_b(self):
                return self._b
            b = property(_get_b)

        >>> o = A()
        >>> trysetattr(A, "a", 1, possible=True)
        >>> trysetattr(A, "b", 1, False)
        AssertionError

    """
    if possible == True:
        a1 = True
        a2 = False
    else:
        a1 = False
        a2 = True
    try:
        setattr(this, attrname, value)
        assert a1  # if the setattr is possible, this should be True
    except Exception:
        assert a2


class TempFile(object):
    """A small wrapper around tempfile.NamedTemporaryFile function

    ::

        f = TempFile(suffix="csv")
        f.name
        f.delete() # alias to delete=False and close() calls


    """

    def __init__(self, suffix="", dir=None):
        self.temp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False, dir=dir)

    def delete(self):
        try:
            self.temp._closer.delete = True
        except:  # pragma: no cover
            self.temp.delete = True
        self.temp.close()

    def _get_name(self):
        return self.temp.name

    name = property(_get_name)

    def __exit__(self, type, value, traceback):
        try:
            self.delete()
        except AttributeError:  # pragma: no cover
            pass
        finally:
            self.delete()

    def __enter__(self):
        return self
