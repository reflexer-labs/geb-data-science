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

# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
#
# Here's a generator that yields the chunks you want:
#
# def chunks(l, n):
#    """Yield successive n-sized chunks from l."""
#    for i in range(0, len(l), n):
#        yield l[i:i+n]
#
# The issue here is that the chunks are not evenly sized chunks
#

__all__ = ["split_into_chunks"]


try:
    range = xrange  # py2
except:
    pass  # py3


def split_into_chunks(items, maxchunks=10):
    """Split a list evenly into N chunks

    .. doctest::

        >>> from easydev import split_into_chunks
        >>> data = [1,1,2,2,3,3]
        >>> list(split_into_chunks(data, 3))
        [[1, 2], [1, 3], [2, 3]]


    """
    chunks = [[] for _ in range(maxchunks)]
    for i, item in enumerate(items):
        chunks[i % maxchunks].append(item)
    return filter(None, chunks)
