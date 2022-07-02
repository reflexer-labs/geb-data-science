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
import argparse


__all__ = ["SmartFormatter"]


class SmartFormatter(argparse.HelpFormatter):
    """Formatter to be used with argparse ArgumentParser

    When using the argparse Python module one can design
    standalone applications with arguments (e.g; --help, --verbose...)

    One can easily define the help as well. However, The help message
    is wrapped by ArgumentParser, removing all formatting in the process.
    The reason being that  the entire documentation is consistent.

    Sometines, one want to keep the format. This class can be used to
    do that.

    Example::

        import argparse
        from easydev import SmartFormatter
        class Options(argparse.ArgumentParser):
        def  __init__(self, prog="sequana"):
            usage = "blabla"
            description="blabla"
            super(Options, self).__init__(usage=usage, prog=prog,
                description=description,
                formatter_class=SmartFormatter)

    """

    def _split_lines(self, text, width):
        if text.startswith("FORMAT|"):
            return text[7:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)
