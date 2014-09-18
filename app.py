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
from sikre.resources.services import ServicesResource, AddServicesResource
from sikre.resources.tests import TestResource
from sikre.resources.login import AuthResource
from sikre import settings

# Add the current directory to the python path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Fire the models module, that will create the models if they don't exist
import sikre.models.models

# Set the headers for all requests... I don't know if this should go here...
def headers_for_all(req, resp, params):
    resp.set_headers({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, x-auth-user, x-auth-password, Authorization',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE'
    })

# Create the API instance, referenced internally as api and externally as
# wsgi_app
api = falcon.API(before=[headers_for_all])

# URLs
api_version = '/' + settings.DEFAULT_API
api.add_route(api_version + '/auth/{provider}/login', LoginResource())
api.add_route(api_version + '/auth/{provider}/logout', LogoutResource())
api.add_route(api_version + '/auth/forgotpassword', ForgotPasswordResource())

api.add_route(api_version + '/items', ItemsResource())
#api.add_route(api_version + '/items/{pk}', ItemsResource())

api.add_route(api_version + '/services', AddServicesResource())
api.add_route(api_version + '/services/{pk}', ServicesResource())

if settings.DEBUG:
    api.add_route('/test_api', TestResource())

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
