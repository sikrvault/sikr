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
from urllib import urlencode
from urllib.parse import parse_qsl

import falcon
import requests
from requests_oauthlib import OAuth1Session

from sikre import settings
from sikre.models.users import User
from sikre.resources.auth import utils
from sikre.utils.logs import logger


class TwitterAuth(object):

    def on_post(self, req, res):

        """Create Twitter JWT token
        """
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        authenticate_url = 'https://api.twitter.com/oauth/authenticate'

        if req.args.get('oauth_token') and req.args.get('oauth_verifier'):
            auth = OAuth1Session(settings.TWITTER_KEY,
                                 client_secret=settings.TWITTER_SECRET,
                                 resource_owner_key=req.args.get('oauth_token'),
                                 verifier=req.args.get('oauth_verifier'))
            r = requests.post(access_token_url, auth=auth)
            profile = dict(parse_qsl(r.text))

            user = User.select().where(User.twitter == profile['user_id']).get()
            if user:
                token = utils.create_jwt_token(user)
                return json.dumps({"token": token})
            u = User(twitter=profile['user_id'],
                     display_name=profile['screen_name'])
            token = utils.create_jwt_token(u)
            return json.dumps({"token": token})
        else:
            oauth = OAuth1Session(settings.TWITTER_KEY,
                                  client_secret=settings.TWITTER_SECRET,
                                  callback_uri=settings.TWITTER_CALLBACK_URI)
            r = requests.post(request_token_url, auth=oauth)
            oauth_token = dict(parse_qsl(r.text))
            qs = urlencode(dict(oauth_token=oauth_token['oauth_token']))
            return redirect(authenticate_url + '?' + qs)

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

    def on_get(self, req, res):
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
