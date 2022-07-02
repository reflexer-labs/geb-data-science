# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of the easydev software
#  It is a modified version of console.py from the sphinx software
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
"""Format colored consoled output. Modified from sphinx.util.console"""
import os
import sys
import platform

__all__ = ["color_terminal", "get_terminal_width", "term_width_line"]


try:
    plf = platform.platform.lower()
    if plf.starstwith("win"):  # pragma: no cover
        import colorama

        colorama.init()
except AttributeError:
    pass

# colors and other functions from the attributes codes are added dynamically to
# this __all__ variable
codes = {}


def get_terminal_width():
    """Returns the current terminal width"""
    try:
        import termios, fcntl, struct

        call = fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack("hhhh", 0, 0, 0, 0))
        _, width = struct.unpack("hhhh", call)[:2]
        terminal_width = width
    except (SystemExit, KeyboardInterrupt):  # pragma: no cover
        raise
    except:
        # FALLBACK
        terminal_width = int(os.environ.get("COLUMNS", 80)) - 1
    return terminal_width


def term_width_line(text):
    """prints pruned version of the input text (limited to terminal width)

    :param str text:
    :return str text:
    """
    _tw = get_terminal_width()
    if not codes:
        # if no coloring, don't output fancy backspaces
        return text + "\n"
    else:
        return text.ljust(_tw) + "\r"


def color_terminal():
    """Does terminal allows coloring

    :return: boolean"""
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    if "COLORTERM" in os.environ:  # pragma: no cover
        return True
    term = os.environ.get("TERM", "dumb").lower()
    if term in ("xterm", "linux") or "color" in term:
        return True
    return False


def __nocolor():  # pragma: no cover
    """set color codes off"""
    codes.clear()


def __coloron():  # pragma: no cover
    """Set color codes on"""
    codes.update(_orig_codes)


def _colorize(name, text):
    return codes.get(name, "") + text + codes.get("reset", "")


def _create_color_func(name):
    def inner(text):
        return _colorize(name, text)

    globals()[name] = inner


_attrs = {
    "reset": "39;49;00m",
    "bold": "01m",
    "faint": "02m",
    "standout": "03m",
    "underline": "04m",
    "blink": "05m",
}

for _name, _value in _attrs.items():
    codes[_name] = "\x1b[" + _value

_colors = [
    ("black", "darkgray"),
    ("darkred", "red"),
    ("darkgreen", "green"),
    ("brown", "yellow"),
    ("darkblue", "blue"),
    ("purple", "fuchsia"),
    ("turquoise", "teal"),
    ("lightgray", "white"),
]

for i, (dark, light) in enumerate(_colors):
    codes[dark] = "\x1b[%im" % (i + 30)
    codes[light] = "\x1b[%i;01m" % (i + 30)

_orig_codes = codes.copy()

for _name in codes:
    _create_color_func(_name)

# dynamically set the colors
for x in codes.keys():
    __all__.append(x)
