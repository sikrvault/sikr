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
