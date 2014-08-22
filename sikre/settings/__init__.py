# Copyright 2014 Clione Software and Havas Worldwide London
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

DEBUG = True
STAGING = False

__version__ = '0.0.1'
__codename__ = 'Kaneda'
__status__ = 'alpha'

if DEBUG and not STAGING:
    from .development import *
elif STAGING:
    from .staging import *
elif not DEBUG and not STAGING:
    from .production import *
