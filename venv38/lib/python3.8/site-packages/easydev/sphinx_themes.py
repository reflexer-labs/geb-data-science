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
"""Common tools to ease access to a easydev sphinx themes."""
import os
from os.path import join as pj

__all__ = ["get_path_sphinx_themes", "get_sphinx_themes"]


def get_path_sphinx_themes():
    """Returns the path where the sphinx themes can be found

    .. doctest::

        >>> from easydev import sphinx_themes
        >>> themes_path = sphinx_themes.get_path_sphinx_themes()

    """
    import easydev

    sharedir = easydev.get_shared_directory_path("easydev")
    sharedir = os.path.join(sharedir, "themes")
    return sharedir


def get_sphinx_themes():
    """Returns the sphinx themes found in easydev

    .. doctest::

        >>> from easydev import sphinx_themes
        >>> themes = sphinx_themes.get_sphinx_themes()
        >>> "standard" in themes
        True

    """
    from easydev import get_shared_directory_path

    sharedir = get_shared_directory_path("easydev")
    sharedir = pj(sharedir, "themes")
    themes = [x for x in os.listdir(sharedir) if x.startswith(".") == False]
    return themes
