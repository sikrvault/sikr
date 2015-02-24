# Copyright 2014-2015 Clione Software and Havas Worldwide London
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Install script for sikre
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
if sys.version_info <= (3, 0):
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
except Exception as e:
    print(" ERROR: Couldn't install Cython, message: {e}".format(e))
    sys.exit(1)
print(" * Cython installed, installing the rest of dependencies....")
try:
    pip.main(['install', '-qr', REQUIREMENTS])
except Exception as e:
    print(" * Couldn't install dependencies. Retry with `pip install -r requirements.txt")
    sys.exit(1)
