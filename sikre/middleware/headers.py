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

import re

import falcon

from sikre import settings
from sikre.utils.logs import logger


class BaseHeaders(object):
    expression = re.compile("^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$")

    def process_request(self, req, res):

        """Process the request before entering in the API

        Before we process anything in the API, we reset the Origin header to
        match the address from the request.

        Args:
            Access-Control-Allow-Origin: Change the origin to the URL that made
                the request.

        Raises:
            HTTP Error: An HTTP error in case the Origin header doesn't match
                        the predefined regular expression.

        Return:
            HTTP headers: A modified set of headers.

        """

        origin_domain = req.get_header('Origin')
        logger.debug("Origin domain is: {}, type: {}".format(origin_domain, type(origin_domain)))
        res.set_headers([
            ('Cache-Control', 'no-store, must-revalidate, no-cache, max-age=0'),
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Access-Control-Allow-Credentials', 'true'),
            ('Access-Control-Allow-Origin', origin_domain),
            ('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, x-auth-user, x-auth-password, Authorization'),
            ('Access-Control-Allow-Methods', 'GET, PUT, POST, OPTIONS, DELETE')
        ])

    def process_response(self, req, res, resource):

        """Process the response before returning it to the client.

        In the reutrning reponse we change some values to be able to overcome
        the CORS protection and mask the origin server. The CORS interaction
        is protected by a check agains a regular expression to make sure the
        origin is a website-like URL.

        Warning:
            If you are really concerned about security, you can deactivate
            the CORS allowance by turning CORS_ACTIVE to `False` in your settings
            file. That will force the application to answer to the SITE_DOMAIN
            domain.

        Args:
            Server (string): Changes the server name sent to the browser in the
                response to avoid exposure of name and version of the same.
            Access-Control-Allow-Origin (string): Change the origin name to
                match the one that made the request. That way we can allow CORS
                anywhere.

        Raises:
            HTTP Error: An HTTP error in case the Origin header doesn't match
            the predefined regular expression.

        Returns:
            HTTP headers: A modified set of headers
        """

        origin_domain = req.get_header('Origin')
        logger.debug("Origin domain is: {}, type: {}".format(origin_domain, type(origin_domain)))
        res.set_headers([
            ('Cache-Control', 'no-store, must-revalidate, no-cache, max-age=0'),
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Server', settings.SERVER_NAME),
            ('Access-Control-Allow-Credentials', 'true'),
            ('Access-Control-Allow-Origin', [origin_domain if settings.CORS_ACTIVE else settings.SERVER_NAME]),
            ('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, x-auth-user, x-auth-password, Authorization'),
            ('Access-Control-Allow-Methods', 'GET, PUT, POST, OPTIONS, DELETE')
        ])
