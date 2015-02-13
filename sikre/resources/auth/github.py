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

import requests

from sikre import settings
from sikre.db.connector import db
from sikre.models.users import User
from sikre.resources.auth import decorators, utils


class GithubAuth(object):

    def on_post(self, req, res):
        access_token_url = 'https://github.com/login/oauth/access_token'
        users_api_url = 'https://api.github.com/user'

        # Read the incoming data
        stream = req.stream.read()
        data = json.loads(stream.decode('utf-8'))

        params = {
            'client_id': data['clientId'],
            'redirect_uri': data['redirectUri'],
            'client_secret': settings.GITHUB_SECRET,
            'code': data['code']
        }

        # Step 1. Exchange authorization code for access token.
        r = requests.get(access_token_url, params=params)
        access_token = dict(parse_qsl(r.text))
        headers = {'User-Agent': 'Satellizer'}

        # Step 2. Retrieve information about the current user.
        r = requests.get(users_api_url, params=access_token, headers=headers)
        print(r)
        profile = json.loads(r.text)
        print(profile)

        # Step 3. (optional) Link accounts.
        if req.auth:
            user = User.select().where(User.github == profile['id']).get()
            if user:
                res = json.dumps(message='There is already a GitHub account that belongs to you')
                res.status_code = 409
                return res

            payload = utils.parse_token(req)

            user = User.select().where(id=payload['sub']).get()
            if not user:
                res = json.dumps(message='User not found')
                res.status_code = 400
                return res

            u = User(github=profile['id'], display_name=profile['name'])
            db.session.add(u)
            db.session.commit()
            token = utils.create_token(u)
            return json.dumps(token=token)

        # Step 4. Create a new account or return an existing one.
        user = User.select().where(github=profile['id']).get()
        if user:
            token = utils.create_token(user)
            return json.dumps(token=token)

        u = User(github=profile['id'], display_name=profile['name'])
        db.session.add(u)
        db.session.commit()
        token = utils.create_token(u)
        return json.dumps(token=token)
