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

import falcon

from sikre import settings


class RequireHTTPS(object):

    """Force the connection to be HTTPS.

    Middleware that intercepts all the requests and checks that is over an HTTPS
    protocol before continuing. The only exception to this is the DEBUG mode,
    in which we allow connections from non-HTTPS sources.

    Raises:
        HTTP Bad Request: If the connection is not HTTPS the API will complain

    Returns:
        JSON: Error mentioning the HTTPS connection is required
    """
    def process_request(self, req, resp):
        if req.protocol == "http" and not settings.DEBUG:
            raise falcon.HTTPBadRequest(title="Client error. HTTP Not Allowed",
                                        description="API connections over HTTPS only.",
                                        href=settings.__docs__)
