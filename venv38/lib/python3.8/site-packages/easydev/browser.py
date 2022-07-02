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
"""Universal browser

This module provides a browser in 2 flavours: as a program to use in a Terminal,
or as a Python function that can be used in other software. The underlying code is based on the standard python module :mod:`webbrowser`. With webbrowser module itself, you can already open a URL as follows in a command line interface::

        python -m webbrowser -t "http://www.python.org"

However, with **browse**, you can simply type::

        browse http://www.python.org

It does not seem to be a big improvments but it is a bit more flexible. First,
there is no need to enter "http://" : it will be added if missing and if this is not a local file.::

    browse docs.python.org
    browse http://docs.python.org --verbose

Similarly, you can open an image (it uses the default image viewer)::

    browse image.png

Or a txt file (or any document provided there is a default executable 
to open it). It works like a charm under Linux. Under MAC, it uses the **open**
command so this should also work.

When invoking **browse**, under MacOSX, it actually tries to call **open**
first and then calls webbrowser, if unsuccessful only. Note tested under
Windows but uses webbrowser is used and works for open HTML document and URLs.

You can also look at a directory (starts nautilus under Fedora)::

    browse ~/Pictures

See more examples below. 

The interest of **browse** is that it can also be used programmatically::

    from easydev.browser import browse
    # open an image with the default image viewer:
    browse("image.png")
    # or a web page
    browse("http://www.uniprot.org")

There is also an alias **onweb**::

    from easydev import onweb

"""
import os
import sys, webbrowser
from optparse import OptionParser
import argparse


def browse(url, verbose=True):
    from sys import platform as _platform

    if _platform == "linux" or _platform == "linux2":
        _browse_linux(url, verbose=True)
    elif _platform == "darwin":  # pragma: no cover
        # under Mac, it looks like the standard  webbrowser may not work as smoothly
        # OS X
        _browse_mac(url, verbose)
    elif _platform == "win32":  # pragma: no cover
        # for windows and others, the same code as Linux should work
        _browse_linux(url, verbose=True)
    else:
        _browse_linux(url, verbose=True)  # pragma: no cover


def _browse_mac(url, verbose=True):  # pragma: no cover
    if verbose:
        print("openning %s" % url)

    import os

    try:
        os.system("open /Applications/Safari.app {}".format(url))
        return
    except:
        pass

    try:
        os.system("open /Applications/Safari.app {}".format("http://" + url))
        return
    except:
        pass

    try:
        webbrowser.open_new(url)
    except:
        if verbose:
            print("Could not open %s. Trying to append http://" % url)
        try:
            webbrowser.open_new("open http://{}".format(url))
        except:
            print("Could not open http://%s" % url)
            raise Exception


def _browse_linux(url, verbose=True):  # pragma: no cover
    if verbose:
        print("openning %s" % url)
    try:
        webbrowser.open(url)
        return
    except:
        pass

    try:
        if verbose:
            print("Could not open %s" % url)
        webbrowser.open("http://" + url)
        return
    except:
        pass

    raise Exception("Could not open http://{}".format(url))


def main(args=None):  # pragma: no cover
    if args is None:
        args = sys.argv[:]

    # check for verbosity
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")
        print(args)
    else:
        verbose = False

    if "--help" in args or len(args) == 1:
        print("Browse, a simple command line browser")
        print("Author: Thomas Cokelaer, (c) 2012.")
        print("USAGE\n\tbrowse http://docs.python.org ")
        print("\tbrowse http://docs.python.org --verbose")
        print("\tbrowse localfile.html")
        print("\tbrowse local_directory (Linux only ?)")
        return
    url = args[1]

    if os.path.exists(url):
        if verbose:
            print("%s is local file. Trying to open it.\n" % url)
        browse(url, verbose)
    else:
        if verbose:
            print("%s seems to be a web address. Trying to open it.\n" % url)
        if url.startswith("http"):
            browse(url, verbose)
        else:
            if verbose:
                print(
                    "%s does not exists and does not starts with http, trying anyway."
                    % url
                )
            browse("http://" + url, verbose)


if __name__ == "__main__":  # pragma: no cover
    import sys

    main(sys.argv)
