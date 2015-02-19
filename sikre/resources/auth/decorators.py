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


def login_required(req, res, resource, params):

    """Check the token to validate login state

    Check the JWT token sent by the frontend to see if the following conditions
    are NOT met:
        - Issuer host doesn't match the one specified in the settings file
        - Expiry timestamp is lower than the current timestamp
        - Issued timestamp is lower than the current timestamp minus SESSION_EXPIRES

    :returns: Redirect to the LOGIN_URL or HTTP 200
    """
    if req.auth:
        logger.debug("Login required: The user has a token in the header")
        payload = utils.parse_token(req)
        current_time = datetime.datetime.now()
        issue_time = current_time - datetime.timedelta(hours=settings.SESSION_EXPIRES)
        if payload['iss'] != settings.SITE_DOMAIN or \
           payload['exp'] <= int(current_time.timestamp()) or \
           payload['iat'] <= int(issue_time):

            logger.debug("Auth token expired of malformed")
            res.body = (
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                '<title>Redirecting...</title>\n'
                '<h1>Redirecting...</h1>\n'
                '<p>You should be redirected automatically to target URL: '
                '<a href="{0}">{0}</a>.  If not click the link.'.format(settings.LOGIN_URL)
            )
            res.location = settings.LOGIN_URL
            res.status = falcon.HTTP_301
            return
        else:
            res.status = falcon.HTTP_200
    else:
        logger.debug("Auth token expired of malformed")
        res.body = (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
            '<title>Redirecting...</title>\n'
            '<h1>Redirecting...</h1>\n'
            '<p>You should be redirected automatically to target URL: '
            '<a href="{0}">{0}</a>.  If not click the link.'.format(settings.LOGIN_URL)
        )
        res.location = settings.LOGIN_URL
        res.status = falcon.HTTP_301
        return
