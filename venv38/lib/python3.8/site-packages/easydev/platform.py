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
from __future__ import absolute_import  # avoids conflict with standard module
import os
import sys

__all__ = ["get_platform"]


def get_platform():  # pragma: no cover
    """Identify the platform (Linux/windows/Mac)

    The folloing modules/functions can be used to identify the platform:
    platform, sys.platform, os.name, os.environ. We use platform and return
    the content of platform.system. If it does not work, sys.platform is used
    and sys.platform output interpreted: linux, java, win and darwin are
    searched for and returned aas Linux, Java, Windows, Darwin to be consistent
    with the output of platform.syste. If those strings are not found,
    just return the output of sys.platform.

    :return: 'Linux' or 'Windows' or 'Darwin', 'Java' if platform
        can be determined otherwise, the content of sys.platform()

    """
    print("//easydev.get_platform() Will be deprecated in future version of easydev")
    try:
        platform = plf.system()
        return platform
    except:
        # platform is not available under all systems (e.g., WLST tool
        # see http://stackoverflow.com/questions/1854/python-what-os-am-i-running-on
        # so, let us try sys.platform
        platform = sys.platform
        if platform.startswith("linux"):
            platform = "Linux"
        elif platform.startswith("java"):
            platform = "Java"
        elif platform.startswith("win"):
            platform = "Windows"
        elif platform.startswith("darwin"):
            platform = "Darwin"
        else:
            print("platform not parsed. Return raw value of sys.platform.")
    return platform


def is_windows():
    if get_platform() == "Windows":
        return True
    else:
        return False


def is_linux():
    if get_platform() == "Linux":
        return True
    else:
        return False


def is_mac():
    if get_platform() == "Mac":
        return True
    else:
        return False
