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

import falcon
import json

from sikre import settings


class VersionResource(object):

    def on_get(self, request, response):

        """Return the version of the API"""
        response.status = falcon.HTTP_200
        response.body = json.dumps({"api_version": settings.__version__,
                                    "version_name": settings.__codename__,
                                    "status": settings.__status__,
                                    "documentation": settings.__docs__})

    def on_post(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The POST method is not allowed in this endpoint.")

    def on_put(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The PUT method is not allowed in this endpoint.")

    def on_update(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The UPDATE method is not allowed in this endpoint.")

    def on_delete(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The DELETE method is not allowed in this endpoint.")
