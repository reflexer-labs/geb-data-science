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
"""This module is a copy of a sphinx extension. unknown origin.

    added by Thomas Cokelaer: get_copybutton_path function.

    Create a sphinx extension based on copybutton javascript from python website

Requires sphinx to be installed. imports are inside functions so not stricly
speaking required for the installation.
"""
import os
from os.path import join as pj
import shutil

try:
    from docutils import nodes
except Exception:  # pragma: no cover
    # if docutils is not installed
    class Dummy:
        SkipNode = Exception

    nodes = Dummy()


__all__ = [
    "get_copybutton_path",
]


def copy_javascript_into_static_path(static="_static", filepath="copybutton.js"):
    """This script can be included in a sphinx configuration file to copy the
    copybutton in the static directory

    :param str static: name of the static path (_static by default)
    :param filename: full path of the file to copy

    :Details: If the path *static* does not exists, it is created. If the
        filename in filepath is already in the path *static*, nothing need to be done.
        Otherwise, the file is copied in *static* directory.

    """
    if os.path.isdir(static):
        pass
    else:
        os.mkdir(static)

    filename = os.path.split(filepath)[1]
    if os.path.isfile(static + os.sep + filename):
        pass
    else:
        shutil.copy(filepath, static + os.sep + filename)


def get_copybutton_path():
    """Return the path where the to find the copybutton javascript

    Copy the copybutton.js javascript in the share directory of easydev so
    that it is accesible by all packages that required it by typing:

    .. doctest::

        >>> from easydev import get_copybutton_path
        >>> p = get_copybutton_path()

    It can then be added with a Sphinx configuration file::

        jscopybutton_path = easydev.copybutton.get_copybutton_path()

    """
    import easydev

    try:  # install mode
        packagedir = easydev.__path__[0]
        packagedir = os.path.realpath(pj(packagedir, "share"))
        os.listdir(packagedir)  # if this faisl, we are in deve mode
    except OSError:  # pragma: no cover
        try:
            packagedir = easydev.__path__[0]
            packagedir = os.path.realpath(pj(packagedir, "..", "share"))
        except:
            raise IOError("could not find data directory")
    return pj(packagedir, "copybutton.js")


def setup(app):  # pragma: no cover
    cwd = os.getcwd()

    # From Sphinx, we typing "make html", this is the place where we expect
    # the JS to be found
    staticpath = os.sep.join([cwd, "source", "_static"])
    from easydev.tools import mkdirs

    mkdirs(staticpath)
    if os.path.exists(staticpath + os.sep + "copybutton.js"):
        pass  # the JS file is already there.
    else:
        # Not found, so let us copy it
        import shutil

        shutil.copy(get_copybutton_path(), staticpath)

    # Now that the file is available, use it
    app.add_js_file("copybutton.js")
