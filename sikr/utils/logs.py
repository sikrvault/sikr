"""Log activator for the platform.

This module activates the logging mechanism of the platform. It must be
imported in all modules that need to declare logs.
"""

import logging
import logging.config

from sikre import settings

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("sikr")
