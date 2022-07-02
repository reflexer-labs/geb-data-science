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
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


import os


__all__ = ["CustomConfig", "DynamicConfigParser", "ConfigExample", "load_configfile"]

#  53, 59, 64-65, 181, 260, 262, 267-270, 288-290, 329, 332-337, 340-341, 359-360, 386-388, 400-401, 406-426, 431-435


class _DictSection(object):
    """Dictionary section.

    Reference: https://gist.github.com/dangoakachan/3855920

    """

    def __init__(self, config, section):
        object.__setattr__(self, "_config", config)
        object.__setattr__(self, "_section", section)

    def __getattr__(self, attr):
        return self.get(attr, None)

    __getitem__ = __getattr__

    def get(self, attr, default=None):
        if attr in self:
            return self._config.get(self._section, attr)
        else:  # pragma: no cover
            return default

    def __setattr__(self, attr, value):
        if attr.startswith("_"):
            object.__setattr__(self, attr, value)
        else:  # pragma: no cover
            self.__setitem__(attr, value)

    def __setitem__(self, attr, value):
        if self._section not in self._config:  # pragma: no cover
            self._config.add_section(self._section)

        self._config.set(self._section, attr, str(value))

    def __delattr__(self, attr):
        if attr in self:
            self._config.remove_option(self._section, attr)

    __delitem__ = __delattr__

    def __contains__(self, attr):
        config = self._config
        section = self._section

        return config.has_section(section) and config.has_option(section, attr)


class ConfigExample(object):
    """Create a simple example of ConfigParser instance to play with

    ::

        >>> from easydev.pipeline.config import ConfigExample
        >>> c = ConfigExample().config  # The ConfigParser instance
        >>> assert 'General' in c.sections()
        >>> assert 'GA' in c.sections()

    This example builds up a ConfigParser instance from scratch.

    This is equivalent to having the following input file::

        [General]
        verbose = True
        tag = test

        [GA]
        popsize = 1


    which can be read with ConfigParser as follows:

    .. doctest::

        >>> # Python 3 code
        >>> from configparser import ConfigParser
        >>> config = ConfigParser()
        >>> config.read("file.ini")
        []

    """

    def __init__(self):
        self.config = ConfigParser()
        self.config.add_section("General")
        self.config.set("General", "verbose", "true")
        self.config.add_section("GA")
        self.config.set("GA", "popsize", "50")


class DynamicConfigParser(ConfigParser, object):
    """Enhanced version of Config Parser

    Provide some aliases to the original ConfigParser class and
    new methods such as :meth:`save` to save the config object in a file.

    .. code-block:: python

        >>> from easydev.config_tools import ConfigExample
        >>> standard_config_file = ConfigExample().config
        >>> c = DynamicConfigParser(standard_config_file)
        >>>
        >>> # then to get the sections, simply type as you would normally do with ConfigParser
        >>> c.sections()
        >>> # or for the options of a specific sections:
        >>> c.get_options('General')

    You can now also directly access to an option as follows::

        c.General.tag

    Then, you can add or remove sections (:meth:`remove_section`, :meth:`add_section`),
    or option from a section :meth:`remove_option`. You can save the instance into a file
    or print it::

        print(c)

    .. warning:: if you set options manually (e.G. self.GA.test =1 if GA is a
        section and test one of its options), then the save/write does not work
        at the moment even though if you typoe self.GA.test, it has the correct value


    Methods inherited from ConfigParser are available:

    ::

        # set value of an option in a section
        c.set(section, option, value=None)
        # but with this class, you can also use the attribute
        c.section.option = value

        # set value of an option in a section
        c.remove_option(section, option)
        c.remove_section(section)


    """

    def __init__(self, config_or_filename=None, *args, **kargs):

        object.__setattr__(self, "_filename", config_or_filename)
        # why not a super usage here ? Maybe there were issues related
        # to old style class ?
        ConfigParser.__init__(self, *args, **kargs)

        if isinstance(self._filename, str) and os.path.isfile(self._filename):
            self.read(self._filename)
        elif isinstance(config_or_filename, ConfigParser):
            self._replace_config(config_or_filename)
        elif config_or_filename == None:
            pass
        else:
            raise TypeError(
                "config_or_filename must be a valid filename or valid ConfigParser instance"
            )

    def read(self, filename):
        """Load a new config from a filename (remove all previous sections)"""
        if os.path.isfile(filename) == False:
            raise IOError("filename {0} not found".format(filename))

        config = ConfigParser()
        config.read(filename)

        self._replace_config(config)

    def _replace_config(self, config):
        """Remove all sections and add those from the input config file

        :param config:

        """
        for section in self.sections():
            self.remove_section(section)

        for section in config.sections():
            self.add_section(section)
            for option in config.options(section):
                data = config.get(section, option)
                self.set(section, option, data)

    def get_options(self, section):
        """Alias to get all options of a section in a dictionary

        One would normally need to extra each option manually::

            for option in config.options(section):
                config.get(section, option, raw=True)#

        then, populate a dictionary and finally take care of the types.

        .. warning:: types may be changed .For instance the string "True"
            is interpreted as a True boolean.

        ..  seealso:: internally, this method uses :meth:`section2dict`
        """
        return self.section2dict(section)

    def section2dict(self, section):
        """utility that extract options of a ConfigParser section into a dictionary

        :param ConfigParser config: a ConfigParser instance
        :param str section: the section to extract

        :returns: a dictionary where key/value contains all the
            options/values of the section required

        Let us build up  a standard config file:
        .. code-block:: python

            >>> # Python 3 code
            >>> from configparser import ConfigParser
            >>> c = ConfigParser()
            >>> c.add_section('general')
            >>> c.set('general', 'step', str(1))
            >>> c.set('general', 'verbose', 'True')

        To access to the step options, you would write::

            >>> c.get('general', 'step')

        this function returns a dictionary that may be manipulated as follows::

            >>> d_dict.general.step

        .. note:: a value (string) found to be True, Yes, true,
            yes is transformed to True
        .. note:: a value (string) found to be False, No, no,
            false is transformed to False
        .. note:: a value (string) found to be None; none,
            "" (empty string) is set to None
        .. note:: an integer is cast into an int
        """
        options = {}
        for option in self.options(section):  # pragma no cover
            data = self.get(section, option, raw=True)
            if data.lower() in ["true", "yes"]:
                options[option] = True
            elif data.lower() in ["false", "no"]:
                options[option] = False
            elif data in ["None", None, "none", ""]:
                options[option] = None
            else:
                try:  # numbers
                    try:
                        options[option] = self.getint(section, option)
                    except:
                        options[option] = self.getfloat(section, option)
                except:  # string
                    options[option] = self.get(section, option, raw=True)
        return options

    def save(self, filename):
        """Save all sections/options to a file.

        :param str filename: a valid filename

        ::

            config = ConfigParams('config.ini') #doctest: +SKIP
            config.save('config2.ini') #doctest: +SKIP

        """
        try:
            if os.path.exists(filename) == True:
                print("Warning: over-writing %s " % filename)
            fp = open(filename, "w")
        except Exception as err:  # pragma: no cover
            print(err)
            raise Exception("filename could not be opened")

        self.write(fp)
        fp.close()

    def add_option(self, section, option, value=None):
        """add an option to an existing section (with a value)

        .. code-block:: python

            >>> c = DynamicConfigParser()
            >>> c.add_section("general")
            >>> c.add_option("general", "verbose", True)
        """
        assert section in self.sections(), "unknown section"
        # TODO I had to cast to str with DictSection
        self.set(section, option, value=str(value))

    def __str__(self):
        str_ = ""
        for section in self.sections():
            str_ += "[" + section + "]\n"
            for option in self.options(section):
                data = self.get(section, option, raw=True)
                str_ += option + " = " + str(data) + "\n"
            str_ += "\n\n"

        return str_

    def __getattr__(self, key):
        return _DictSection(self, key)

    __getitem__ = __getattr__

    def __setattr__(self, attr, value):
        if attr.startswith("_") or attr:
            object.__setattr__(self, attr, value)
        else:
            self.__setitem__(attr, value)

    def __setitem__(self, attr, value):
        if isinstance(value, dict):
            section = self[attr]
            for k, v in value.items():
                section[k] = v
        else:
            raise TypeError("value must be a valid dictionary")

    def __delattr__(self, attr):
        if attr in self:
            self.remove_section(attr)

    def __contains__(self, attr):
        return self.has_section(attr)

    def __eq__(self, data):
        # FIXME if you read file, the string "True" is a string
        # but you may want it to be converted to a True boolean value
        if sorted(data.sections()) != sorted(self.sections()):
            print("Sections differ")
            return False
        for section in self.sections():

            for option in self.options(section):
                try:
                    if str(self.get(section, option, raw=True)) != str(
                        data.get(section, option, raw=True)
                    ):
                        print("option %s in section %s differ" % (option, section))
                        return False
                except:  # pragma: no cover
                    return False
        return True


class CustomConfig(object):
    """Base class to manipulate a config directory"""

    def __init__(self, name, verbose=False):
        self.verbose = verbose
        from easydev import appdirs

        self.appdirs = appdirs.AppDirs(name)

    def init(self):
        sdir = self.appdirs.user_config_dir
        self._get_and_create(sdir)

    def _get_config_dir(self):
        sdir = self.appdirs.user_config_dir
        return self._get_and_create(sdir)

    user_config_dir = property(
        _get_config_dir, doc="return directory of this configuration file"
    )

    def _get_and_create(self, sdir):
        if not os.path.exists(sdir):
            print("Creating directory %s " % sdir)
            try:
                self._mkdirs(sdir)
            except Exception:  # pragma: no cover
                print("Could not create the path %s " % sdir)
                return None
        return sdir

    def _mkdirs(self, newdir, mode=0o777):
        """See :func:`easydev.tools.mkdirs`"""
        from easydev.tools import mkdirs

        mkdirs(newdir, mode)

    def remove(self):
        try:
            sdir = self.appdirs.user_config_dir
            os.rmdir(sdir)
        except Exception as err:  # pragma: no cover
            raise Exception(err)


def _load_configfile(configpath):  # pragma: no cover
    "Tries to load a JSON or YAML file into a dict."
    try:
        with open(configpath) as f:
            try:
                import json

                return json.load(f)
            except ValueError:
                f.seek(0)  # try again
            try:
                import yaml
            except ImportError:
                raise IOError(
                    "Config file is not valid JSON and PyYAML "
                    "has not been installed. Please install "
                    "PyYAML to use YAML config files."
                )
            try:
                return yaml.load(f, Loader=yaml.FullLoader)
            except yaml.YAMLError:
                raise IOError(
                    "Config file is not valid JSON or YAML. "
                    "In case of YAML, make sure to not mix "
                    "whitespace and tab indentation."
                )
    except Exception as err:
        raise (err)


def load_configfile(configpath):
    "Loads a JSON or YAML configfile as a dict."
    config = _load_configfile(configpath)
    if not isinstance(config, dict):
        raise IOError(
            "Config file must be given as JSON or YAML " "with keys at top level."
        )
    return config
