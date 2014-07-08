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

from peewee import *
import falcon
import json

from talons.auth import middleware
from talons.auth import basicauth, httpheader, htpasswd

import settings

# Define the database connection and get the cursor for operating
db = peewee
conn = sqlite3.connect('test.db')
db = conn.cursor()


# Assume getappconfig() returns a dictionary of application configuration
# options that may have been read from some INI file...
# config = getappconfig()

# auth_middleware = middleware.create_middleware(identify_with=[
#                                                  basicauth.Identifier,
#                                                  httpheader.Identifier],
#                                                authenticate_with=htpasswd.Authenticator,
#                                                **config)


class Item(object):

    def on_get(self, request, response):
        """
        Handle the GET request, returning a list of the items that the user
        has access to.
        """
        response.status = falcon.HTTP_200
        response.body = "Hello data!"


class Service(object):

    def on_get(self, request, response):
        pass

    def on_post(self, request, response):
        pass


# Create the API instance, referenced internally as api and externally as
# wsgi_app
wsgi_app = api = falcon.API()

items = Item()
api.add_route('/items', items)
