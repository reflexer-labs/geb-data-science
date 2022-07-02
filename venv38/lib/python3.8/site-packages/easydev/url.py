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
"""Utilities related to the web"""
try:
    import httplib
except ImportError:
    import http.client as httplib


__all__ = ["isurl_reachable"]


def isurl_reachable(url, timeout=10, path="/"):  # pragma: no cover
    """Checks if an URL exists or nor

    :param str url: the url to look for
    :param str path: Used in request.request at the
        url path following the domain name. For instance,
        www.ensembl.org is the site url but actually
        we want to check this full url www.ensembl.org/biomart/martview
    :return: True if it exists

    .. versionchanged:: 0.9.30
    """
    if url.startswith("http://") or url.startswith("https://"):
        url = url.split("//")[1]
    conn = httplib.HTTPConnection(url, timeout=timeout)
    try:
        conn.request("HEAD", path)
    except:
        return False
    # 302 is a redirection
    # 200 is okay
    try:
        response = conn.getresponse()
    except:
        return False

    if response.status in [200, 302]:
        return True
    else:
        return False
