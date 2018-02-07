"""Main system checks of the platform.

In this module are located the functions to perform the system cheks to
guarantee that the platform will run correctly.
"""

import sys


def check_python():
    """Check that the python version is no less than 3.5.x."""
    if sys.version_info <= (3, 5):
        sys.stdout.write("\nSorry, requires Python 3.5.x or better.\n")
        sys.exit(1)
