# -*- python -*-
#
#  This file is part of easydev software
#
#  Copyright (c) 2012-2014
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: https://github.com/cokelaer/easydev
#
##############################################################################
# import logging
import colorlog

__all__ = ["Logging"]


colors = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}


class Logging(object):
    """logging utility.

    ::

        >>> l = Logging("root", "INFO")
        >>> l.info("test")
        INFO:root:test
        >>> l.level = "WARNING"
        >>> l.info("test")

    """

    def __init__(self, name="root", level="WARNING", text_color="blue"):
        self._name = name
        self.formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s[%(name)s:%(lineno)d]: %(reset)s %({})s%(message)s".format(
                text_color
            ),
            datefmt=None,
            reset=True,
            log_colors=colors,
            secondary_log_colors={},
            style="%",
        )
        self._set_name(name)

        logger = colorlog.getLogger(self._name)
        handler = colorlog.StreamHandler()
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)

    def _set_name(self, name):
        level = self.level
        self._name = name
        logger = colorlog.getLogger(self._name)
        if level == 0:
            self._set_level("WARNING")
        else:
            self._set_level(level)

    def _get_name(self):
        return self._name

    name = property(_get_name, _set_name)

    def _set_level(self, level):
        if isinstance(level, bool):
            if level is True:
                level = "INFO"
            if level is False:
                level = "ERROR"
        if level == 10:
            level = "DEBUG"
        if level == 20:
            level = "INFO"
        if level == 30:
            level = "WARNING"
        if level == 40:
            level = "ERROR"
        if level == 50:
            level = "CRITICAL"
        colorlog.getLogger(self.name).setLevel(level)

    def _get_level(self):
        level = colorlog.getLogger(self.name).level
        if level == 10:
            return "DEBUG"
        elif level == 20:
            return "INFO"
        elif level == 30:
            return "WARNING"
        elif level == 40:
            return "ERROR"
        elif level == 50:
            return "CRITICAL"
        else:
            return level

    level = property(_get_level, _set_level)

    def debug(self, msg):
        colorlog.getLogger(self.name).debug(msg)

    def info(self, msg):
        colorlog.getLogger(self.name).info(msg)

    def warning(self, msg):
        colorlog.getLogger(self.name).warning(msg)

    def critical(self, msg):
        colorlog.getLogger(self.name).critical(msg)

    def error(self, msg):
        colorlog.getLogger(self.name).error(msg)
