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

import json

import falcon

from sikre import settings


class VersionResource(object):

    """Returns the API version details

    Args:
        object
    Returns:
        JSON data
    """

    def on_get(self, request, response):

        """Return the version of the API"""
        response.status = falcon.HTTP_200
        response.body = json.dumps({"api_version": settings.__version__,
                                    "api_codename": settings.__codename__,
                                    "api_status": settings.__status__,
                                    "documentation": settings.__docs__})

    def on_post(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(request.method),
                               href=settings.__docs__)

    def on_put(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(request.method),
                               href=settings.__docs__)

    def on_update(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(request.method),
                               href=settings.__docs__)

    def on_delete(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(request.method),
                               href=settings.__docs__)
