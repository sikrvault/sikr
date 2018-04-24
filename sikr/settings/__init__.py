"""Settings selector.

This module decides which settings module to load depending on the DEBUG and
STAGING settings. These two setings can be defined from the local environment
using values of 0 (False) and 1 (True).
"""

import os

DEBUG = bool(int(os.getenv('SIKR_IS_DEBUG', True)))
STAGING = bool(int(os.getenv('SIKR_IS_STAGING', False)))

__version__ = '0.0.1'
__codename__ = 'Kaneda'
__status__ = 'alpha'
__docs__ = 'http://docs.sikr.io'

if DEBUG and not STAGING:
    from .development import *
elif STAGING:
    from .staging import *
elif not DEBUG and not STAGING:
    from .production import *
