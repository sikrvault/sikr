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

import falcon

from sikre.middleware import json, https, headers, handle_404, auth
from sikre.resources import groups, items, services, main, tests
from sikre.resources.auth import github, facebook, google, twitter, linkedin
from sikre.utils.logs import logger
from sikre.utils.checks import check_python
from sikre import settings

check_python()

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        from sikre.db import generator, syncdb, superuser
        if sys.argv[1] == "syncdb":
            syncdb.generate_db_schema()
        if sys.argv[1] == "createsuperuser":
            superuser.create_superuser()
        if sys.argv[1] == "generate":
            user = superuser.create_superuser()
            generator.generate_database(user=user)
    else:
        print("No option specified.\n\n"
              "    syncdb          - Create the database schema\n"
              "    createsuperuser - Create a superuser account"
              "    generate        - Fill the database with random data. Useful for testing\n\n"
              "If you intended to run the application itself you must call the constructor\n"
              "in the following fashion (uwsgi example):\n\n"
              "    uwsgi --http :8080 --wsgi-file app.py --callable api\n\n")
else:
    # Create the API instance, referenced internally as api and externally as
    # wsgi_app
    api = falcon.API(
        media_type='application/json',
        middleware=[
            auth.LoginRequired(),
            # json.RequireJSON(),
            # json.JSONTranslator(),
            https.RequireHTTPS(),
            headers.BaseHeaders(),
            handle_404.WrongURL()
        ]
    )

    # URLs
    api_version = '/' + settings.DEFAULT_API
    api.add_route(api_version, main.APIInfo())

    # Basic Auth
    # api.add_route(api_version + '/auth/login', auth.LoginResource())
    # api.add_route(api_version + '/auth/logout', LogoutResource())
    # api.add_route(api_version + '/auth/forgotpassword', ForgotPasswordResource())

    # Social Auth
    api.add_route(api_version + '/auth/facebook/login', facebook.FacebookAuth())
    api.add_route(api_version + '/auth/google/login', google.GoogleAuth())
    api.add_route(api_version + '/auth/twitter/login', twitter.TwitterAuth())
    api.add_route(api_version + '/auth/github/login', github.GithubAuth())
    api.add_route(api_version + '/auth/linkedin/login', linkedin.LinkedinAuth())

    # Content
    api.add_route(api_version + '/groups', groups.Groups())
    api.add_route(api_version + '/groups/{id}', groups.DetailGroup())
    api.add_route(api_version + '/items', items.Items())
    api.add_route(api_version + '/items/{id}', items.DetailItem())
    api.add_route(api_version + '/services', services.Services())
    api.add_route(api_version + '/services/{id}', services.DetailService())

    logger.debug("API service started")

    if settings.DEBUG:
        api.add_route('/test_api', tests.TestResource())
