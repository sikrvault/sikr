"""Main application functions.

This file is the core of the application and it defines the intantiation of the
API and their URLs, as well as some extra functionality if it's run from the
command line to generate or syncronize the database.
"""

import sys

import falcon

from sikre.middleware import json, https, headers, handle_404
from sikre.resources import categories, items, services, main, tests, sharing
from sikre.resources.auth import github, facebook, google, twitter, linkedin
from sikre.utils.logs import logger
from sikre.utils.checks import check_python
from sikre import settings

check_python()

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        from sikre.db import generator, syncdb
        if sys.argv[1] == "syncdb":
            syncdb.generate_db_schema()
        if sys.argv[1] == "generate":
            if settings.DEBUG:
                generator.generate_database()
            else:
                sys.exit(" * `generate` command not available when "
                         "DEBUG=False. Please set DEBUG=True and remember "
                         "to install the development requirements.")
    else:
        print("No option specified.\n\n"
              "    syncdb          - Create the database schema\n"
              "    generate        - Fill the database with random data.\n\n"
              "If you intended to run the application itself you must call "
              "the constructor\n"
              "in the following fashion (uwsgi example):\n\n"
              "    uwsgi --http :8080 --wsgi-file app.py --callable api\n\n")
else:
    # Create the API instance, referenced internally as api and externally as
    # wsgi_app
    api = falcon.API(
        media_type='application/json; charset=utf-8',
        middleware=[
            json.RequireJSON(),
            json.JSONTranslator(),
            https.RequireHTTPS(),
            headers.BaseHeaders(),
            handle_404.WrongURL()
        ]
    )

    # URLs
    api_version = '/' + settings.DEFAULT_API
    api.add_route(api_version, main.APIInfo())

    # Social Auth
    api.add_route(api_version + '/auth/facebook/login', facebook.FacebookAuth())
    api.add_route(api_version + '/auth/google/login', google.GoogleAuth())
    api.add_route(api_version + '/auth/twitter/login', twitter.TwitterAuth())
    api.add_route(api_version + '/auth/github/login', github.GithubAuth())
    api.add_route(api_version + '/auth/linkedin/login', linkedin.LinkedinAuth())

    # Content
    api.add_route(api_version + '/categories', categories.Categories())
    api.add_route(api_version + '/categories/{id}', categories.DetailCategory())
    api.add_route(api_version + '/items', items.Items())
    api.add_route(api_version + '/items/{id}', items.DetailItem())
    api.add_route(api_version + '/services', services.Services())
    api.add_route(api_version + '/services/{id}', services.DetailService())

    # Sharing
    api.add_route(api_version + '/share', sharing.Share())

    logger.debug("API service started")

    if settings.DEBUG:
        api.add_route('/test_api', tests.TestResource())
