# Copyright 2014 Clione Software and Havas Worldwide London
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

import falcon

from sikre.models.models import User


def create_jwt_token(user):
    payload = {
        'iss': 'localhost',
        'sub': user.id,
        'iat': datetime.now(),
        'exp': datetime.now() + timedelta(days=14)
    }
    token = jwt.encode(payload, app.config['TOKEN_SECRET'])
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['TOKEN_SECRET'])


class LoginResource(object):

    """
    The login resource handles the login from all the
    """
    def on_get(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_post(self, request, response):

        """
        This method will check that the email and the token match, then logs
        in the user.
        """
        print("WHATEVER: " + request)
        try:
            user = User.get(username=request.body['username'])
            valid = user.check_password(request.body['password'])
            print("WHATEVER: " + request)
            if valid:
                pass
            response.statuc = falcon.HTTP_200
            response.body = 'Logged in'
        except:
            raise falcon.HTTPError(falcon.HTTP_500)


    def on_put(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_update(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The UPDATE method is not allowed in this endpoint.")

    def on_delete(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The DELETE method is not allowed in this endpoint.")


class LogoutResource(object):

    """
    The login resource handles the login from all the
    """
    def on_get(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_post(self, request, response, provider):

        """
        This method will check that the email and the token match, then logs
        in the user.
        """

        response.statuc = falcon.HTTP_200
        response.body = 'whatever, man'

    def on_put(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_update(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The UPDATE method is not allowed in this endpoint.")

    def on_delete(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The DELETE method is not allowed in this endpoint.")

class ForgotPasswordResource(object):

    """
    The login resource handles the login from all the
    """
    def on_get(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_post(self, request, response, provider):

        """
        This method will check that the email and the token match, then logs
        in the user.
        """

        response.statuc = falcon.HTTP_200
        response.body = 'whatever, man'

    def on_put(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_update(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The UPDATE method is not allowed in this endpoint.")

    def on_delete(self, request, response, provider):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The DELETE method is not allowed in this endpoint.")
