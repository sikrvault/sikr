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
from requests_oauthlib import OAuth1Session

from sikre import settings
from sikre.models.users import User
from sikre.resources.auth import utils
from sikre.utils.logs import logger


class LinkedinAuth(object):

    def on_post(self, req, res):

        @app.route('/auth/linkedin', methods=['POST'])
        def linkedin():
            access_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
            people_api_url = 'https://api.linkedin.com/v1/people/~:(id,first-name,last-name,email-address)'

            payload = dict(client_id=request.json['clientId'],
                           redirect_uri=request.json['redirectUri'],
                           client_secret=app.config['LINKEDIN_SECRET'],
                           code=request.json['code'],
                           grant_type='authorization_code')

            # Step 1. Exchange authorization code for access token.
            r = requests.post(access_token_url, data=payload)
            access_token = json.loads(r.text)
            params = dict(oauth2_access_token=access_token['access_token'],
                          format='json')

            # Step 2. Retrieve information about the current user.
            r = requests.get(people_api_url, params=params)
            profile = json.loads(r.text)

            user = User.query.filter_by(linkedin=profile['id']).first()
            if user:
                token = create_token(user)
                return jsonify(token=token)
            u = User(linkedin=profile['id'],
                     display_name=profile['firstName'] + ' ' + profile['lastName'])
            db.session.add(u)
            db.session.commit()
            token = create_token(u)
            return jsonify(token=token)

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
