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

import datetime

import falcon

from sikre import settings
from sikre.resources.auth import utils
from sikre.utils.logs import logger


class LoginRequired(object):

    """Force all endpoints to require a valid token before serving data.
    """
    def process_request(self, req, res):
        if req.auth:
            logger.debug("The user has a token in the header")
            payload = utils.parse_token(req)
            current_time = datetime.datetime.now()
            issue_time = current_time - datetime.timedelta(hours=settings.SESSION_EXPIRES)
            if payload['iss'] != settings.SITE_DOMAIN or \
               payload['exp'] <= int(current_time.timestamp()) or \
               payload['iat'] <= int(issue_time.timestamp()):

                logger.debug("JWT token expired or malformed")
                raise falcon.HTTPError(falcon.HTTP_401, title="Credentials expired",
                                       description="Your crendentials have expired. Please login again.")

            else:
                res.status = falcon.HTTP_200
        else:
            logger.debug("No JWT token found")
            raise falcon.HTTPError(falcon.HTTP_401, title="Credentials not found",
                                   description="You don't have the credentials to access this resource")
