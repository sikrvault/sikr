#!/usr/bin/env python

"""Main application functions.

This file is the core of the application and it defines the intantiation of the
API and their URLs, as well as some extra functionality if it's run from the
command line to generate or syncronize the database.
"""

import sys
import argparse

import falcon

from sikr.middleware import json, https, headers, handle_404
from sikr.resources import categories, items, services, main, tests, sharing
from sikr.resources.auth import github, facebook, google, twitter, linkedin
from sikr.utils.logs import logger
from sikr.utils.checks import check_python
from sikr import settings

check_python()

# If the aplication is run directly through terminal, run this.
if __name__ == "__main__":
    from sikr.db import generator, syncdb

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="If you are trying to run the "
                                     "application itself, you must call "
                                     "the constructor \nin the following "
                                     "fashion (uWSGI example):\n\n"
                                     "uwsgi --http :8080 --wsgi-file app.py --callable api \n\n")
    parser.add_argument("-s", "--syncdb", help="Create the database schema",
                        action="store_true")
    parser.add_argument("-g", "--generate", help="Fill the database with random data",
                        action="store_true")
    args = parser.parse_args()

    # If there's no input print help
    if not len(sys.argv) > 1:
        parser.print_help()

    if args.syncdb:
        syncdb.generate_db_schema()
    if args.generate:
        if not settings.DEBUG:
            sys.stdout.write("\n`generate` command is not available when debug "
                             " mode is active. Please set DEBUG=True in the "
                             "settings to use it.\n")
        else:
            generator.generate_database()
# Else create the API instance, referenced as api
else:
    api = falcon.API(
        media_type='application/json; charset=UTF-8',
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
