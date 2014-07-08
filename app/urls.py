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

from app.models import User, Group, Item, Service
import settings

import falcon

# Create the API instance, referenced internally as api and externally as
# wsgi_app
wsgi_app = api = falcon.API()

import app.urls

items = Item()
groups = Group()
users = User()
services = Service()

api.add_route('/{}/items'.format(settings.DEFAULT_API), items)
api.add_route('/{}/users'.format(settings.DEFAULT_API), users)
api.add_route('/{}/groups'.format(settings.DEFAULT_API), groups)
api.add_route('/{}/services'.format(settings.DEFAULT_API), services)