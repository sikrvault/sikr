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

import sys


def check_python():

    """Check that the python version is no less than 3.3.x
    """
    # Check if we are running on python 3.3 or greater
    if sys.version_info <= (3, 3):
        sys.stdout.write("\nSorry, requires Python 3.3.x or better.\n")
        sys.exit(1)
