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
# from urllib.parse import parse_qsl

import falcon
import requests

from sikre import settings
from sikre.models.users import User
from sikre.resources.auth import utils
from sikre.utils.logs import logger


class GoogleAuth(object):

    def on_post(self, req, res):
        access_token_url = 'https://accounts.google.com/o/oauth2/token'
        people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

        # Read the incoming data
        stream = req.stream.read()
        data = json.loads(stream.decode('utf-8'))
        logger.debug("Google OAuth: Incoming data read successfully")

        payload = {
            'client_id': data['clientId'],
            'redirect_uri': data['redirectUri'],
            'client_secret': settings.GOOGLEPLUS_SECRET,
            'code': data['code'],
            'grant_type': 'authorization_code'
        }
        logger.debug("Google OAuth: Built the code response correctly")

        # dict(client_id=request.json['clientId'],
        #                redirect_uri=request.json['redirectUri'],
        #                client_secret=app.config['GOOGLE_SECRET'],
        #                code=request.json['code'],
        #                grant_type='authorization_code')

        # Step 1. Exchange authorization code for access token.
        r = requests.post(access_token_url, data=payload)
        token = json.loads(r.text)
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
        logger.debug("Google OAuth: Auth code exchange for token success")

        # Step 2. Retrieve information about the current user.
        r = requests.get(people_api_url, headers=headers)
        profile = json.loads(r.text)
        logger.debug("Google OAuth: Retrieve user information success")

        try:
            user = User.select().where(User.google == profile['sub']).get()
            if user:
                logger.debug("Google OAuth: Account {0} already exists".format(profile["sub"]))
                token = utils.create_jwt_token(user)
                res.body = json.dumps({"token": token})
                res.status = falcon.HTTP_200
                return
        except User.DoesNotExist:
            logger.debug("Google OAuth: User does not exist")
            user = User.create(google=profile['sub'], username=profile['name'])
            user.save()
            logger.debug("Google OAuth: Created user {0}".format(profile["name"]))
            token = utils.create_jwt_token(user)
            res.body = json.dumps({"token": token})
            res.status = falcon.HTTP_200
            return

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
# class GoogleAuth(object):
#     access_token_url = 'https://accounts.google.com/o/oauth2/token'
#     people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

#     payload = dict(client_id=request.json['clientId'],
#                    redirect_uri=request.json['redirectUri'],
#                    client_secret=app.config['GOOGLE_SECRET'],
#                    code=request.json['code'],
#                    grant_type='authorization_code')

#     # Step 1. Exchange authorization code for access token.
#     r = requests.post(access_token_url, data=payload)
#     token = json.loads(r.text)
#     headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

#     # Step 2. Retrieve information about the current user.
#     r = requests.get(people_api_url, headers=headers)
#     profile = json.loads(r.text)

#     user = User.query.filter_by(google=profile['sub']).first()
#     if user:
#         token = create_jwt_token(user)
#         return jsonify(token=token)
#     u = User(google=profile['sub'],
#              first_name=profile['given_name'],
#              last_name=profile['family_name'])
#     db.session.add(u)
#     db.session.commit()
#     token = create_jwt_token(u)
#     return jsonify(token=token)
