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
# from sikr.resources import categories, items, services, main, tests, sharing
# from sikr.resources.auth import github, facebook, google, twitter, linkedin
from sikr.resources import main
from sikr.utils.logs import logger
from sikr.utils.checks import check_python
from sikr import settings

check_python()

# If the aplication is run directly through terminal, run this.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="If you are trying to run the "
        "application itself, you must call "
        "the constructor \nin the following "
        "fashion (uWSGI example):\n\n"
        "uwsgi --http :8080 --wsgi-file app.py --callable api \n\n")
    parser.add_argument("-s", "--syncdb",
                        help="Create the database schema",
                        action="store_true")
    parser.add_argument("-g", "--generate",
                        help="Fill the database with random data",
                        action="store_true")
    args = parser.parse_args()

    # If there's no input print help
    if not len(sys.argv) > 1:
        parser.print_help()

    if args.syncdb:
        from sikr.db.syncdb import generate_schema
        generate_schema()

    if args.generate:
        if not settings.DEBUG:
            print("\n`generate` command is not available when debug "
                  " mode is disabled. Please set DEBUG=True in the "
                  "settings to use it.\n")
        else:
            print('In development')
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
    logger.debug("API service started")
