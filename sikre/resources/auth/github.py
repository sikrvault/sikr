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

from sikre.resources.auth import decorators, utils
from sikre import settings


class GithubAuth(object):

    def on_post(self, req, res):
        access_token_url = 'https://github.com/login/oauth/access_token'
        users_api_url = 'https://api.github.com/user'

        params = {
            'client_id': req.json['clientId'],
            'redirect_uri': req.json['redirectUri'],
            'client_secret': settings.GITHUB_SECRET,
            'code': req.json['code']
        }

        # Step 1. Exchange authorization code for access token.
        r = req.get(access_token_url, params=params)
        access_token = dict(parse_qsl(r.text))
        headers = {'User-Agent': 'Satellizer'}

        # Step 2. Retrieve information about the current user.
        r = req.get(users_api_url, params=access_token, headers=headers)
        profile = json.loads(r.text)

        # Step 3. (optional) Link accounts.
        if req.headers.get('Authorization'):
            user = User.select().where(github=profile['id']).get()
            if user:
                res = jsonify(message='There is already a GitHub account that belongs to you')
                res.status_code = 409
                return res

            payload = parse_token(req)

            user = User.select().where(id=payload['sub']).get()
            if not user:
                res = jsonify(message='User not found')
                res.status_code = 400
                return res

            u = User(github=profile['id'], display_name=profile['name'])
            db.session.add(u)
            db.session.commit()
            token = create_token(u)
            return jsonify(token=token)

        # Step 4. Create a new account or return an existing one.
        user = User.select().where(github=profile['id']).get()
        if user:
            token = create_token(user)
            return jsonify(token=token)

        u = User(github=profile['id'], display_name=profile['name'])
        db.session.add(u)
        db.session.commit()
        token = create_token(u)
        return jsonify(token=token)
