import falcon

from sikr import settings


class RequireHTTPS(object):

    """Force the connection to be HTTPS.

    Middleware that intercepts all the requests and checks that is over an HTTPS
    protocol before continuing. The only exception to this is the DEBUG mode,
    in which we allow connections from non-HTTPS sources.

    Raises:
        HTTP Bad Request: If the connection is not HTTPS the API will complain

    Returns:
        JSON: Error mentioning the HTTPS connection is required
    """
    def process_request(self, req, resp):
        if req.protocol == "http" and not settings.DEBUG:
            raise falcon.HTTPBadRequest(title="Client error. HTTP Not Allowed",
                                        description="API connections over HTTPS only.",
                                        href=settings.__docs__)
