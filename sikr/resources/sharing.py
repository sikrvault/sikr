import json

import falcon

from sikr import settings
from sikr.utils.logs import logger
from sikr.models.users import User
from sikr.models.services import Service
from sikr.models.shares import ShareToken
from sikr.resources.auth.decorators import login_required
from sikr.resources.auth.utils import parse_token
from sikr.utils.tokens import generate_token


class Share(object):

    """Share a object from the platform with someone
    """
    @falcon.before(login_required)
    def on_post(self, req, res):
        try:
            # Parse token and get user id
            user_id = parse_token(req)['sub']
            # Get the user
            user = User.get(User.id == int(user_id))
        except Exception as e:
            logger.error("Can't verify user")
            raise falcon.HTTPBadRequest(title="Bad request",
                                        description=e,
                                        href=settings.__docs__)

        try:
            raw_json = req.stream.read()
            logger.debug("Got incoming JSON data")
        except Exception as e:
            logger.error("Can't read incoming data stream")
            raise falcon.HTTPBadRequest(title="Bad request",
                                        description=e,
                                        href=settings.__docs__)

        try:
            result_json = json.loads(raw_json.decode("utf-8"), encoding='utf-8')
            logger.debug(result_json)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')

        try:
            new_share = ShareToken(user=user, token=generate_token(),
                                   resource=int(result_json.get()))
        except:
            pass

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

    def on_get(self, req, res, pk):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_put(self, req, res, pk):
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
