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
from urllib.parse import parse_qsl

import falcon
import requests

from sikre import settings
from sikre.models.users import User
from sikre.resources.auth import utils
from sikre.utils.logs import logger


class GithubAuth(object):

    def on_post(self, req, res):

        """Create the JWT token for the user
        """
        access_token_url = 'https://github.com/login/oauth/access_token'
        users_api_url = 'https://api.github.com/user'

        # Read the incoming data
        stream = req.stream.read()
        data = json.loads(stream.decode('utf-8'))
        logger.debug("GitHub OAuth: Incoming data read successfully")

        params = {
            'client_id': data['clientId'],
            'redirect_uri': data['redirectUri'],
            'client_secret': settings.GITHUB_SECRET,
            'code': data['code']
        }
        logger.debug("GitHub OAuth: Built the code response correctly")

        # Step 1. Exchange authorization code for access token.
        r = requests.get(access_token_url, params=params)
        access_token = dict(parse_qsl(r.text))
        headers = {'User-Agent': 'Satellizer'}
        logger.debug("GitHub OAuth: Auth code exchange for token success")

        # Step 2. Retrieve information about the current user.
        r = requests.get(users_api_url, params=access_token, headers=headers)
        profile = json.loads(r.text)
        logger.debug("GitHub OAuth: Retrieve user information success")

        # Step 3. (optional) Link accounts.
        if req.auth:
            payload = utils.parse_token(req)
            try:
                user = User.select().where(
                    (User.github == profile['id']) |
                    (User.id == payload['sub']) |
                    (User.email == profile['email'])
                ).get()
                # Set the github code again. This is a failsafe.
                user.github = profile['id']
                user.save()
                logger.debug("GitHub OAuth: Account {0} already exists".format(profile["id"]))
            except User.DoesNotExist:
                logger.debug("GitHub OAuth: User does not exist")
                user = User.create(github=profile['id'], username=profile['name'], email=profile["email"])
                user.save()
                logger.debug("GitHub OAuth: Created user {0}".format(profile["name"]))
        else:
            try:
                user = User.select().where(
                    (User.github == profile['id']) |
                    (User.email == profile['email'])
                ).get()
                # Set the github code again. This is a failsafe.
                user.github = profile['id']
                user.save()
            except User.DoesNotExist:
                logger.debug("GitHub OAuth: User does not exist")
                user = User.create(github=profile['id'], username=profile['name'], email=profile["email"])
                user.save()
                logger.debug("GitHub OAuth: Created user {0}".format(profile["name"]))
        token = utils.create_jwt_token(user)
        res.body = json.dumps({"token": token})
        res.status = falcon.HTTP_200

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
