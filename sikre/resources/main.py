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

import json

import falcon

from sikre import settings


class APIInfo(object):

    """Show the main information about the API like endpoints, version, etc.
    """

    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = json.dumps(
            {
                "endpoints": {
                    "facebook_login": settings.DEFAULT_API + '/auth/facebook/login',
                    "google_login": settings.DEFAULT_API + '/auth/google/login',
                    "github_login": settings.DEFAULT_API + '/auth/github/login',
                    "twitter_login": settings.DEFAULT_API + '/auth/twitter/login',
                    "linkedin_login": settings.DEFAULT_API + '/auth/linkedin/login',
                    "groups": settings.DEFAULT_API + '/groups',
                    "group_detail": settings.DEFAULT_API + '/groups/{id}',
                    "items": settings.DEFAULT_API + '/items',
                    "item_detail": settings.DEFAULT_API + '/items/{id}',
                    "services": settings.DEFAULT_API + '/services',
                    "service_detail": settings.DEFAULT_API + '/services/{id}',
                },
                "version": {
                    "api_version": settings.__version__,
                    "api_codename": settings.__codename__,
                    "api_status": settings.__status__,
                    "documentation": settings.__docs__
                }
            }
        )

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

    def on_post(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_put(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_update(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_delete(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)
