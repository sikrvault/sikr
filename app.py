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

import sys

import falcon

from sikre.middleware import json, https, headers, handle_404
from sikre.resources import groups, items, services, main, tests
from sikre.utils.logs import logger
from sikre import settings
# Check if we are running on python 3
if sys.version_info <= (3, 0):
    sys.stdout.write("Sorry, requires Python 3.3.x or better, not Python 2.x\n")
    sys.exit(1)

# Fire the models module, that will create the models if they don't exist
import sikre.models.models

# Create the API instance, referenced internally as api and externally as
# wsgi_app
api = falcon.API(
    middleware=[
        json.RequireJSON(),
        https.RequireHTTPS(),
        headers.BaseHeaders(),
        handle_404.WrongURL()
    ]
)

# URLs
api_version = '/' + settings.DEFAULT_API
api.add_route(api_version, main.Version())
# api.add_route(api_version + '/auth/login', auth.LoginResource())
# api.add_route(api_version + '/auth/logout', LogoutResource())

# api.add_route(api_version + '/auth/forgotpassword', ForgotPasswordResource())
# api.add_route(api_version + '/auth/facebook', FacebookAuth())
# api.add_route(api_version + '/auth/google', GoogleAuth())
# api.add_route(api_version + '/auth/twitter', Twitter())
# api.add_route(api_version + '/auth/github', GithubAuth())
# api.add_route(api_version + '/auth/linkedin', LinkedinAuth())

api.add_route(api_version + '/groups', groups.Groups())
api.add_route(api_version + '/groups/{pk}', groups.DetailGroup())
api.add_route(api_version + '/items', items.Items())
api.add_route(api_version + '/item/{pk}', items.DetailItem())
api.add_route(api_version + '/services', services.Services())
api.add_route(api_version + '/services/{pk}', services.DetailService())

logger.debug("API service started")

if settings.DEBUG:
    api.add_route('/test_api', tests.TestResource())
