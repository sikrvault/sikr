"""Installation script for sikr.

This script will make the necessary checks and install the dependencies
according to what the user has selected.

How to use:
    $ python install.py <environment>

    Environments:
        - dev      - Development environment and toolset
        - <other>  - Install the common environment
"""

import os
import sys
import pip

if len(sys.argv) >= 2:
    if sys.argv[1] == 'dev':
        REQUIREMENTS = os.path.join(os.getcwd(), 'requirements/dev.txt')
        print(" * Selected development requirements")
    else:
        REQUIREMENTS = os.path.join(os.getcwd(), 'requirements/common.txt')
        print(" * Selected common requirements")

# Check if we are running on python 3
if sys.version_info <= (3, 3):
    sys.stdout.write(" * Python 3 not detected.")
    sys.stdout.write("sikre requires Python 3.3.x or better\n")
    sys.exit(1)

# Are we running inside a virtual environment?
if hasattr(sys, "real_prefix") or sys.prefix != sys.base_prefix:
    print(" * Virtual environment found")
else:
    print(" * Virtual environment not detected. You will need to "
          "create one through the `pyvenv` command. Exiting.")
    sys.exit(1)

# Let's install cython
print(" * Installing cython... ")
# We can't install anything until cython is finished, the reason is to make
# falcon more efficient by bytecompiling it.
try:
    pip.main(['install', '-q', 'cython'])
    print(" * Cython installed, installing the rest of dependencies....")
except Exception as e:
    print(" ERROR: Couldn't install Cython, message: {e}".format(e))
    sys.exit(1)
try:
    pip.main(['install', '-qr', REQUIREMENTS])
except Exception as e:
    print(" * Couldn't install dependencies. Retry with `pip install"
          " -r requirements/common.txt")
    sys.exit(1)
