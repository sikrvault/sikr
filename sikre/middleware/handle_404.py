import json

import falcon

from sikre import settings


class WrongURL(object):

    def process_response(self, req, resp, resource=''):

        """Intercept main 404 response by Falcon

        If the API hits a non existing endpoint, it will trigger a customized
        404 response that will redirect people to the documentation.

        Raises:
            HTTP 404: A falcon.HTTP_404 error

        Returns:
            JSON: A customized JSON response
        """
        if resp.status == falcon.HTTP_404:
            resp.body = json.dumps({"message": "Resource not found",
                                    "documentation": settings.__docs__})
