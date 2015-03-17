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

import uuid

from sikre.models.shares import ShareToken


def generate_token():

    """Generates a unique token

    Generate a new token based of the HEX version of a UUID and check if it
    already exists. If that's the case generate a new one.
    """
    duplicated = True

    while duplicated:
        try:
            token = uuid.uuid4().hex
            share_token = ShareToken.get(token=token)
            duplicated = True
        except ShareToken.DoesNotExist:
            duplicated = False
            return token
