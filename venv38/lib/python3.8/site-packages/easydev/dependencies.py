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
# $:Id $

import pkg_resources


__all__ = ["get_dependencies"]


def get_dependencies(pkgname):
    """Return dependencies of a package as a sorted list

    :param str pkgname: package name
    :return: list (empty list if no dependencies)
    """
    try:
        res = pkg_resources.require(pkgname)
        res = list(set(res))
        res.sort()
        return res
    except Exception:
        return []
