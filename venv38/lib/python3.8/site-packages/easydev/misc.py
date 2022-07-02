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
import os


__all__ = ["get_home", "cmd_exists"]


def get_home():
    """Return path of the HOME"""
    # This function should be robust
    # First, let us try with expanduser
    try:
        homedir = os.path.expanduser("~")
    except ImportError:  # pragma: no cover
        # This may happen.
        pass
    else:
        if os.path.isdir(homedir):
            return homedir
    # Then, with getenv
    for this in ("HOME", "USERPROFILE", "TMP"):  # pragma: no cover
        # getenv is same as os.environ.get
        homedir = os.environ.get(this)
        if homedir is not None and os.path.isdir(homedir):
            return homedir


def cmd_exists(cmd):
    """Return true if the command do exists in the environement"""
    try:
        import subprocess

        # for unix/max only
        result = subprocess.call(
            "type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result == 0:
            return True
        else:
            return False
    except Exception:  # pragma: no cover
        # If subprocess is not found, we assume it exists.
        # This choice ensure that if it fails, we keep going.
        return True


def in_ipynb():
    """Checks if we are in an ipython notebook

    :return: True if in an ipython notebook otherwise returns False

    """
    try:  # pragma: no cover
        cfg = get_ipython().config
        if (
            "parent_appname" in cfg["IPKernelApp"].keys()
            and cfg["IPKernelApp"]["parent_appname"] == "ipython-notebook"
        ):
            return True
        elif "connection_file" in cfg["IPKernelApp"].keys():
            if "jupyter" in cfg["IPKernelApp"]["connection_file"]:
                return True
        return False
    except NameError:  # pragma: no cover
        return False
