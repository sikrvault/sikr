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
from urllib.parse import parse_qsl, urlencode

import falcon
import requests
from requests_oauthlib import OAuth1

from sikre import settings
from sikre.models.users import User
from sikre.resources.auth import utils
from sikre.utils.logs import logger


class TwitterAuth(object):

    def on_get(self, req, res):

        """Create Twitter JWT token
        """
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        authenticate_url = 'https://api.twitter.com/oauth/authenticate'

        if req.get_param('oauth_token') and req.get_param('oauth_verifier'):
            auth = OAuth1(settings.TWITTER_KEY,
                          client_secret=settings.TWITTER_SECRET,
                          resource_owner_key=req.get_param('oauth_token'),
                          verifier=req.get_param('oauth_verifier'))
            logger.debug("Twitter OAuth: Got auth session. Previous auth.")
            r = requests.post(access_token_url, auth=auth)
            profile = dict(parse_qsl(r.text))
            logger.debug("Twitter OAuth: User profile retrieved")

            try:
                user = User.select().where(User.twitter == profile['user_id'] |
                                           User.username == profile['screen_name']).get()
            except:
                user = User.create(twitter=profile['user_id'],
                                   username=profile['screen_name'])

            token = utils.create_jwt_token(user)
            res.body = json.dumps({"token": token})
            res.status = falcon.HTTP_200
        else:
            oauth = OAuth1(settings.TWITTER_KEY,
                           client_secret=settings.TWITTER_SECRET,
                           callback_uri=settings.TWITTER_CALLBACK_URI)
            logger.debug("Twitter OAuth: Got auth session. No previous auth")
            r = requests.post(request_token_url, auth=oauth)
            oauth_token = dict(parse_qsl(r.text))
            logger.debug("Twitter OAuth: User profile retrieved")
            qs = urlencode(dict(oauth_token=oauth_token['oauth_token']))

            # Falcon doesn't support redirects, so we have to fake it
            # this implementation has been taken from werkzeug
            final_url = authenticate_url + '?' + qs
            res.body = (
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                '<title>Redirecting...</title>\n'
                '<h1>Redirecting...</h1>\n'
                '<p>You should be redirected automatically to target URL: '
                '<a href="{0}">{0}</a>.  If not click the link.'.format(final_url)
            )
            res.location = final_url
            res.status = falcon.HTTP_301

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

    def on_post(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)

    def on_put(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)

    def on_update(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)

    def on_delete(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)
