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

import pkg_resources

try:
    version = pkg_resources.require("easydev")[0].version
except:
    version = ">=0.11.0"


from . import browser
from .browser import browse as onweb

from . import codecs
from .codecs import *

from . import chunks
from .chunks import *

from . import copybutton
from .copybutton import *

from . import decorators
from .decorators import *

from . import doc
from .doc import *

from . import easytest
from .easytest import *

from . import logging_tools
from .logging_tools import *

from . import sphinx_themes
from .sphinx_themes import *

from . import tools
from .tools import *


from .md5tools import md5

from . import options
from .options import *

from . import paths
from .paths import *

from . import misc
from .misc import *

from . import config_tools
from .config_tools import *

# from . import timer
from .timer import Timer

from . import url
from .url import *

# import dependencies
from .dependencies import get_dependencies

from . import multicore
from .multicore import *


from .progressbar import TextProgressBar, progress_bar, Progress


from .profiler import do_profile
