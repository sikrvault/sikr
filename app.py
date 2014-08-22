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

import os

import falcon

from sikre.resources.items import ItemsResource
from sikre.resources.services import ServicesResource
from sikre import settings

# Add the current directory to the python path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Fire the models module, that will create the models if they don't exist
import sikre.models.models

# Create the API instance, referenced internally as api and externally as
# wsgi_app
api = falcon.API()

items = ItemsResource()
# groups = Group()
# users = User()
services = ServicesResource()

api.add_route('/{}/items'.format(settings.DEFAULT_API), items)
# api.add_route('/{}/users'.format(settings.DEFAULT_API), users)
# api.add_route('/{}/groups'.format(settings.DEFAULT_API), groups)
api.add_route('/{}/services'.format(settings.DEFAULT_API), services)

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
