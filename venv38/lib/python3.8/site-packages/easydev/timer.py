# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of the easydev software
#
#  Copyright (c) 2011-2017
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: https://github.com/cokelaer/easydev
#  Documentation: http://easydev-python.readthedocs.io
#
##############################################################################
"""A convenient timer"""
import time


class Timer(object):  # pragma: no cover
    """Timer working with *with* statement

    ::

        times = []
        with Timer(times):
            # do something
            import time
            time.sleep(0.1)
        with Timer(imes):
            # do something else
            time.sleep(0.2)

    """

    def __init__(self, times):
        self.times = times

    def __enter__(self):
        self.t1 = time.time()

    def __exit__(self, type, value, traceback):
        self.t2 = time.time()
        self.times.append(self.t2 - self.t1)
