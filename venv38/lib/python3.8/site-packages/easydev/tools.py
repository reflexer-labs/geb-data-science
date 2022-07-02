#
#  This file is part of the easydev software
#
#  Copyright (c) 2011-2020
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
"""toolkit to ease development"""
import subprocess
import json
import os
import sys


__all__ = [
    "shellcmd",
    "swapdict",
    "check_param_in_list",
    "check_range",
    "precision",
    "AttrDict",
    "DevTools",
    "execute",
    "touch",
    "mkdirs",
]


def precision(data, digit=2):
    """Round values in a list keeping only N digits precision

    ::

        >>> precision(2.123)
        2.12
        >>> precision(2123, digit=-2)
        2100

    """
    data = int(data * pow(10, digit))
    data /= pow(10.0, digit)
    return data


def check_range(value, a, b, strict=False):
    """Check that a value lies in a given range

    :param value: value to test
    :param a: lower bound
    :param b: upper bound
    :return: nothing

    .. doctest::

        >>> from easydev.tools import check_range
        >>> check_range(1,0, 2)

    """
    if strict is True:
        if value <= a:
            raise ValueError(" {} must be greater (or equal) than {}".format(value, a))
        if value >= b:
            raise ValueError(" {} must be less (or less) than {}".format(value, b))
    elif strict is False:
        if value < a:
            raise ValueError(" {} must be greater than {}".format(value, a))
        if value > b:
            raise ValueError(" {} must be less than {}".format(value, b))


def checkParam(param, valid_values):
    """
    .. warning:: deprecated since 0.6.10 use :meth:`check_param_in_list` instead
    """
    print("easydev WARNING:: deprecated; use check_param_in_list instead.")
    check_param_in_list(param, valid_values)


def check_param_in_list(param, valid_values, name=None):
    """Checks that the value of param is amongst valid

    :param param: a parameter to be checked
    :param list valid_values: a list of values

    ::

        check_param_in_list(1, [1,2,3])
        check_param_in_list(mode, ["on", "off"])
    """
    if isinstance(valid_values, list) is False:

        raise TypeError(
            "the valid_values second argument must be a list of valid values. {0} was provided.".format(
                valid_values
            )
        )

    if param not in valid_values:
        if name:
            msg = "Incorrect value provided for {} ({})".format(name, param)
        else:
            msg = "Incorrect value provided (%s)" % param
        msg += "    Correct values are %s" % valid_values
        raise ValueError(msg)


def shellcmd(cmd, show=False, verbose=False, ignore_errors=False):
    """An alias to run system commands with Popen.

    Based on subprocess.Popen.

    :param str cmd: the command to call
    :param bool show: print the command
    :param bool verbose: print the output

    :return: the output as a string
    """
    if show:
        print(cmd)
    try:
        ret = subprocess.Popen(
            [cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        output = ret.stdout.read().strip()
        error = ret.stderr.read().strip()
        ret.wait()

        if len(error) > 0:
            if ignore_errors is False:
                raise Exception(error)
            else:
                if verbose is True:
                    print("Errors/Warning" + str(error))

        if verbose is True:
            print(output)

        return output
    except Exception as err:
        raise Exception("Error:: Command (%s) failed. Error message is %s" % (cmd, err))


def execute(cmd, showcmd=True, verbose=True):
    """An alias to run system commands using pexpect.

    :param cmd:
    :param showcmd:
    :param verbose:
    """
    import pexpect

    if showcmd is True:
        print(cmd)

    p = pexpect.spawn(cmd, timeout=None)
    line = p.readline()
    while line:
        if verbose:
            try:
                sys.stdout.write(line.decode())
            except:
                sys.stdout.write(line)

            sys.stdout.flush()
        line = p.readline()


def touch(fname, times=None):
    """Touch a file (like unix command)"""
    with open(fname, "a"):
        os.utime(fname, times)


def swapdict(dic, check_ambiguity=True):
    """Swap keys for values in a dictionary

    ::

        >>> d = {'a':1}
        >>> swapdict(d)
        {1:'a'}

    """
    # this version is more elegant but slightly slower : return {v:k for k,v in dic.items()}
    if check_ambiguity:
        assert len(set(dic.keys())) == len(
            set(dic.values())
        ), "values is not a set. ambiguities for keys."
    return dict(zip(dic.values(), dic.keys()))


def mkdirs(newdir, mode=0o777):
    """Recursive creation of a directory

    :source: matplotlib mkdirs. In addition, handles "path" without slashes

    make directory *newdir* recursively, and set *mode*.  Equivalent to ::

        > mkdir -p NEWDIR
        > chmod MODE NEWDIR
    """
    # mkdirs("analysis") # without / at the end led to an error
    # since os.path.split returns ('', 'analysis')
    try:
        if not os.path.exists(newdir):
            parts = os.path.split(newdir)
            for i in range(1, len(parts) + 1):
                thispart = os.path.join(*parts[:i])
                # if no sep at the end, thispart may be an empty string
                # so, we need to check if thispart exists and is not of len 0
                if not os.path.exists(thispart) and len(thispart):
                    os.makedirs(thispart, mode)
    except OSError as err:
        import errno

        # Reraise the error unless it's about an already existing directory
        if err.errno != errno.EEXIST or not os.path.isdir(newdir):
            raise


class AttrDict(dict):
    """dictionary-like object that exposes its keys as attributes.

    When you have dictionary of dictionaries with many levels e.g.::

        d = {'a': {'a1': {'a2': 2}}}

    to get/set a values, one has to type something like::

        d['a']['a1']['a2'] = 3

    The :class:`AttrDict` allows the dictionary to work as attributes::

        ad = AttrDict(**d)
        ad.a.a1.a2 = 3

    You can now add values as attribute, or with ['key'] syntax

    .. doctest::

        >>> from easydev import AttrDict
        >>> a = AttrDict(**{'value': 1})
        >>> a.value
        1
        >>>
        >>> a.unit = 'meter'
        >>> sorted(a.keys())
        ['unit', 'value']

    If you need to add new simple values after the creation of the instance,
    just use the setter::

        >>> d['newa'] = 2
        >>> d.newa = 2  # equivalent to the statement above

    but if you want to set a dictionary (whichever recursive level), use
    the :meth:`update` method::

        >>> d.update({'newd': {'g': {'h':2}}})
        >>> d.newd.g.h
        2

    Note that if you use the setter for a value that is a dictionary, e.g.::

        ad.a = {'b':1}

    then *a* is indeed a dictionary.

    """

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self
        self.update(kwargs)

    def update(self, content):
        """See class/constructor documentation for details

        :param dict content: a valid dictionary
        """
        # accepts dict and attrdict classes
        try:
            from collections import OrderedDict
        except:
            OrderedDict = AttrDict

        if content.__class__ not in [dict, OrderedDict, AttrDict]:
            raise TypeError

        for k, v in content.items():
            if v.__class__ not in [dict, AttrDict, OrderedDict]:
                # fixme copy ?
                self[k] = v
            else:
                self[k] = AttrDict(**v)

    def from_json(self, filename):
        """
        does not remove existing keys put replace them if already present
        """
        res = json.load(open(filename, "r"))
        for k, v in res.items():
            self[k] = v

    def to_json(self, filename=None):
        import json

        if filename is not None:
            with open(filename, "w") as fout:
                json.dump(self, fout)
        else:
            return json.dumps(self)


class DevTools(object):
    """Aggregate of easydev.tools functions."""

    def check_range(self, value, a, b):
        """wrapper around :func:`easydev.check_range`"""
        check_range(value, a, b, strict=False)

    def check_param_in_list(self, param, valid_values):
        """wrapper around :func:`easydev.check_param_in_list`"""
        param = self.to_list(param)
        for name in param:
            check_param_in_list(name, list(valid_values))

    def swapdict(self, d):
        """wrapper around :func:`easydev.swapdict`"""
        return swapdict(d)

    def to_list(self, query):
        """Cast to a list if possible

        'a' ->['a']
        1 -> [1]
        """
        from easydev import codecs

        return codecs.to_list(query)

    def list2string(self, query, sep=",", space=False):
        """
        see :func:`easydev.tools.list2string`

        """
        from easydev import codecs

        return codecs.list2string(query, sep=sep, space=space)

    def to_json(self, dictionary):
        """Transform a dictionary to a json object"""
        return json.dumps(dictionary)

    def mkdir(self, dirname):
        """Create a directory if it does not exists; pass without error otherwise"""
        try:
            os.mkdir(dirname)
        except OSError:
            pass  # exists already
        except Exception as err:
            raise (err)

    def shellcmd(self, cmd, show=False, verbose=False, ignore_errors=False):
        """See :func:`shellcmd`"""
        return shellcmd(cmd, show=show, verbose=verbose, ignore_errors=ignore_errors)

    def check_exists(self, filename):
        """Raise error message if the file does not exists"""
        if os.path.exists(filename) is False:
            raise ValueError("This file %s does not exists" % filename)

    def mkdirs(self, dirname, mode=0o777):
        mkdirs(dirname, mode=mode)
