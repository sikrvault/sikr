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

import falcon

from sikre import settings
from sikre.utils.logs import logger
from sikre.models.users import User
from sikre.models.services import Service
from sikre.resources.auth.decorators import login_required
from sikre.resources.auth.utils import parse_token


class ShareGroup(object):

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


class ShareItem(object):

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


class ShareService(object):

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
