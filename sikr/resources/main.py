from datetime import datetime, timezone
import json

import falcon

from sikr import settings


class APIInfo(object):

    """Show the main information about the API like endpoints, version, etc.
    """

    def on_get(self, req, res):
        payload = {
            "version": {
                "api_version": settings.__version__,
                "api_codename": settings.__codename__,
                "api_status": settings.__status__,
                "documentation": settings.__docs__
            },
            "date": str(datetime.utcnow().replace(tzinfo=timezone.utc)),
        }
        res.status = falcon.HTTP_200
        res.body = json.dumps(payload)

    def on_options(self, req, res):
        res.status = falcon.HTTP_200

    def on_post(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_put(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_update(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_delete(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)
