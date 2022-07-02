##############################################################################
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
"""Utilities to ease access to share data paths"""
import os
from os.path import join as pj
import pkg_resources


__all__ = [
    "get_shared_directory_path",
    "get_shared_directories",
    "get_share_file",
    "gsf",
    "get_package_location",
]


def get_package_location(package):
    """Return physical location of a package"""
    try:
        info = pkg_resources.get_distribution(package)
        location = info.location
    except pkg_resources.DistributionNotFound as err:
        print("package provided (%s) not installed." % package)
        raise
    return location


def get_shared_directory_path(package):
    """Returns the share directory path of an installed package


    ::

        sharedir = get_shared_directory_path("easydev")


    """
    location = get_package_location(package)

    # print("install  mode ? ")
    sharedir = os.path.realpath(pj(location, package, "share"))
    if os.path.isdir(sharedir) == True:
        # looks like we have found the share directory so it is an install mode
        # print ("yes")
        return sharedir
    else:  # pragma: no cover
        # print("no. searching for share dir as if in develop mode")
        # let us try a couple of directories
        # FIXME: do we need the 3 cases ??
        # probably just 2 are required, one for develop and one for install mode
        sharedir = os.path.realpath(pj(location, "..", "share"))
        if os.path.isdir(sharedir) == True:
            return sharedir
        sharedir = os.path.realpath(pj(location, "..", "..", "share"))
        if os.path.isdir(sharedir) == True:
            return sharedir
        sharedir = os.path.realpath(pj(location, "..", "..", "..", "share"))
        if os.path.isdir(sharedir) == True:
            return sharedir
        # could not be found,
        sharedir = []
        print("could not find any share directory in %s" % package)

    return sharedir


def get_shared_directories(package, datadir="data"):
    """Returns all directory paths found in the package share/datadir directory

    :param str datadir: scans package/share/<datadir> where datadir is "data" by
        default. If it does not exists, the list returned is empty.

    .. doctest::

        >>> from easydev import get_shared_directories
        >>> shared_directories = get_shared_directories("easydev", "themes")
        >>> len(shared_directories)>=2
        True

    """
    packagedir = get_shared_directory_path(package)
    if len(packagedir) == 0:  # pragma: no cover
        return []
    packagedir = pj(packagedir, datadir)
    directories = os.listdir(packagedir)

    # get rid of .svn (for the packages installed with develop)
    directories_to_process = []
    for directory in directories:
        fullpath = os.path.join(packagedir, directory)
        if directory != ".svn" and os.path.isdir(fullpath):
            directories_to_process.append(fullpath)
    directories_to_process.sort()
    return directories_to_process


def gsf(package, datadir, filename):
    return get_share_file(package, datadir, filename)


def get_share_file(package, datadir, filename):
    """Creates the full path of a file to be found in the share directory of a package"""
    packagedir = get_shared_directory_path(package)
    fullpath = os.path.join(packagedir, datadir)
    # check that it exists
    if os.path.isdir(fullpath) == False:  # pragma: no cover
        raise ValueError(
            "The directory %s in package %s does not seem to exist"
            % (packagedir, fullpath)
        )
    filename_path = os.path.join(fullpath, filename)
    if os.path.isfile(filename_path) == False:
        correct_files = [x for x in os.listdir(fullpath) if os.path.isfile(x)]
        msg = "The file %s does not exists. Correct filenames found in %s/%s are:\n" % (
            filename_path,
            package,
            datadir,
        )
        for f in correct_files:  # pragma: no cover
            msg += "%s\n" % f

        raise ValueError(msg)
    return filename_path
