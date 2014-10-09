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
import logging
import json

from sikre.models.models import User


class LoginResource(object):

    """
    The login resource handles the login from all the
    """
    def __init__(self):
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_post(self, request, response, **kwargs):

        """
        This method will check that the email and the token match, then logs
        in the user.
        """
        print(request.get_param('email'))
        try:
            user = User.get(username=request.get_param('login-email'))
            valid = user.check_password(request.body['login-password'])
            print("WHATEVER: " + request)
            if valid:
                pass
            response.status = falcon.HTTP_200
            response.body = 'Logged in'
        except:
            raise falcon.HTTPError(falcon.HTTP_500)


    def on_put(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_update(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The UPDATE method is not allowed in this endpoint.")

    def on_delete(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The DELETE method is not allowed in this endpoint.")

    def on_options(self, request, response):
        '''
        Handles all OPTIONS requests.
        Returns status code 200.
        '''
        resp.status = falcon.HTTP_200


class LogoutResource(object):

    """
    The login resource handles the login from all the
    """
    def on_get(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_post(self, request, response):

        """
        This method will check that the email and the token match, then logs
        in the user.
        """

        response.status = falcon.HTTP_200
        response.body = 'whatever, man'

    def on_put(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_update(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The UPDATE method is not allowed in this endpoint.")

    def on_delete(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The DELETE method is not allowed in this endpoint.")

class ForgotPasswordResource(object):

    """
    The login resource handles the login from all the
    """
    def on_get(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_post(self, request, response, provider):

        """
        This method will check that the email and the token match, then logs
        in the user.
        """

        response.status = falcon.HTTP_200
        response.body = 'whatever, man'

    def on_put(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_update(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The UPDATE method is not allowed in this endpoint.")

    def on_delete(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The DELETE method is not allowed in this endpoint.")
