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


class Services(object):

    @falcon.before(login_required)
    def on_get(self, req, res):
        """
        """
        # Parse token and get user id
        user_id = parse_token(req)['sub']
        # See if we have to filter by item
        filter_item = req.get_param("item", required=False)

        try:
            # Get the user
            user = User.get(User.id == int(user_id))
            if filter_item:
                services = list(user.allowed_services
                                    .select(Service.id, Service.name,
                                            Service.username, Service.password,
                                            Service.url, Service.port, Service.extra,
                                            Service.ssh_title, Service.ssh_public,
                                            Service.ssh_private, Service.ssl_title,
                                            Service.ssl_filename, Service.other)
                                    .where(Service.item == int(filter_item))
                                    .dicts())
                logger.debug("Got services filtered by item")
            else:
                services = list(user.allowed_services
                                    .select(Service.id, Service.name,
                                            Service.username, Service.password,
                                            Service.url, Service.port, Service.extra,
                                            Service.ssh_title, Service.ssh_public,
                                            Service.ssh_private, Service.ssl_title,
                                            Service.ssl_filename, Service.other)
                                    .dicts())
                logger.debug("Got all the items")
            res.status = falcon.HTTP_200
            res.body = json.dumps(services)
        except Exception as e:
            logger.error(e)
            error_msg = ("Unable to get the services. Please try again later")
            raise falcon.HTTPServiceUnavailable(title=req.method + " failed",
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

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
            new_service = Service.create(name=result_json.get("name"),
                                         item=result_json.get("item"),
                                         username=result_json.get("username", ''),
                                         password=result_json.get("password", ''),
                                         url=result_json.get("url", ''),
                                         port=result_json.get("port", 0),
                                         extra=result_json.get("extra", ''),
                                         ssh_title=result_json.get("ssh_title", ''),
                                         ssh_public=result_json.get("ssh_public", ''),
                                         ssh_private=result_json.get("ssh_private", ''),
                                         ssl_title=result_json.get("ssl_title", ''),
                                         ssl_filename=result_json.get("ssh_title", ''),
                                         other=result_json.get("other", ''))
            new_service.save()
            new_service.allowed_users.add(user)
        except Exception as e:
            raise falcon.HTTPInternalServerError(title="Error while saving the item",
                                                 description=e,
                                                 href=settings.__docs__)

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

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


class DetailService(object):

    """
    This resource handles the /services/ url.
    """
    @falcon.before(login_required)
    def on_get(self, req, res, id):
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
            service = Service.get(Service.id == id)
            if user not in service.allowed_users:
                raise falcon.HTTPForbidden(title="Permission denied",
                                           description="You don't have access to this resource",
                                           href=settings.__docs__)
            # service = list(Service.select(Service.id, Service.name,
            #                               Service.username, Service.password,
            #                               Service.url, Service.port, Service.extra,
            #                               Service.ssh_title, Service.ssh_public,
            #                               Service.ssh_private, Service.ssl_title,
            #                               Service.ssl_filename, Service.other)
            #                       .where(Service.id == id)
            #                       .dicts())
            res.status = falcon.HTTP_200
            res.body = json.dumps(service)
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the items. Please try again later")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    @falcon.before(login_required)
    def on_put(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    @falcon.before(login_required)
    def on_delete(self, req, res, id):
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
            service = Service.get(Service.id == id)
            if user not in service.allowed_users:
                raise falcon.HTTPForbidden(title="Permission denied",
                                           description="You don't have access to this resource",
                                           href=settings.__docs__)
            service.delete_instance()
            res.status = falcon.HTTP_200
            res.body = json.dumps({"message": "Deletion successful"})

        except Exception as e:
            print(e)
            error_msg = ("Unable to delete service. Please try again later.")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_options(self, req, res, id):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

    def on_update(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    @falcon.before(login_required)
    def on_post(self, req, res, id):
        pass
