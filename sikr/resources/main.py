import json

import falcon

from sikr import settings


class APIInfo(object):

    """Show the main information about the API like endpoints, version, etc.
    """

    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = json.dumps(
            {
                "endpoints": {
                    "facebook_login": settings.DEFAULT_API + '/auth/facebook/login',
                    "google_login": settings.DEFAULT_API + '/auth/google/login',
                    "github_login": settings.DEFAULT_API + '/auth/github/login',
                    "twitter_login": settings.DEFAULT_API + '/auth/twitter/login',
                    "linkedin_login": settings.DEFAULT_API + '/auth/linkedin/login',
                    "groups": settings.DEFAULT_API + '/groups',
                    "group_detail": settings.DEFAULT_API + '/groups/{id}',
                    "items": settings.DEFAULT_API + '/items',
                    "item_detail": settings.DEFAULT_API + '/items/{id}',
                    "services": settings.DEFAULT_API + '/services',
                    "service_detail": settings.DEFAULT_API + '/services/{id}',
                },
                "version": {
                    "api_version": settings.__version__,
                    "api_codename": settings.__codename__,
                    "api_status": settings.__status__,
                    "documentation": settings.__docs__
                }
            }
        )

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
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
