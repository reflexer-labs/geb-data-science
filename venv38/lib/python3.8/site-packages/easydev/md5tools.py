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
"""md5 utility"""
import hashlib


def md5(fname, chunk=65536):
    """Return the MD5 checksums of a file

    Takes about 25 seconds on a 8Gb file.
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for this in iter(lambda: f.read(chunk), b""):
            hash_md5.update(this)
    return hash_md5.hexdigest()
