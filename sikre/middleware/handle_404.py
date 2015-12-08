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


class WrongURL(object):

    def process_response(self, req, resp, resource=''):

        """Intercept main 404 response by Falcon

        If the API hits a non existing endpoint, it will trigger a customized
        404 response that will redirect people to the documentation.

        Raises:
            HTTP 404: A falcon.HTTP_404 error

        Returns:
            JSON: A customized JSON response
        """
        if resp.status == falcon.HTTP_404:
            resp.body = json.dumps({"message": "Resource not found",
                                    "documentation": settings.__docs__})
