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
from sikre.models.items import Category
from sikre.resources.auth.decorators import login_required
from sikre.resources.auth.utils import parse_token


class Categories(object):

    """Show all the groups that the current user has read permission.

    This resource will send the Categorys that belong to the user in the
    matter of ID and NAME
    """
    @falcon.before(login_required)
    def on_get(self, req, res):
        # Parse token and get user id
        user_id = parse_token(req)['sub']

        try:
            # Get the user
            user = User.get(User.id == int(user_id))

            groups = list(user.allowed_Categorys
                              .select(Category.id, Category.name)
                              .dicts())
            res.status = falcon.HTTP_200
            res.body = json.dumps(groups)
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the groups. Please try again later")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
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
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')

        try:
            new_Category = Category.create(name=result_json['name'] or '')
            new_Category.save()
            new_Category.allowed_users.add(user)
        except Exception as e:
            raise falcon.HTTPInternalServerError(title="Error while saving the group",
                                                 description=e,
                                                 href=settings.__docs__)

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

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


class DetailCategory(object):

    """Show details of a specific group or add/delete a group
    """
    @falcon.before(login_required)
    def on_get(self, req, res, id):
        user_id = parse_token(req)['sub']
        try:
            user = User.get(User.id == int(user_id))
            group = Category.get(Category.id == int(id))
            if user not in group.allowed_users:
                raise falcon.HTTPForbidden(title="Permission denied",
                                           description="You don't have access to this resource",
                                           href=settings.__docs__)
            res.status = falcon.HTTP_200
            res.body = json.dumps(group)
            logger.debug("Items request succesful")
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the group. Please try again later.")
            raise falcon.HTTPServiceUnavailable(req.method + " failed",
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    @falcon.before(login_required)
    def on_put(self, req, res, id):
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
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect.')
        try:
            group = Category.get(Category.id == int(id))
            if user not in group.allowed_users:
                raise falcon.HTTPForbidden(title="Permission denied",
                                           description="You don't have access to this resource",
                                           href=settings.__docs__)
            group.name = result_json["name"]
            group.save()
            res.status = falcon.HTTP_200
            res.body = json.dumps({"message": "Group updated"})
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the group. Please try again later.")
            raise falcon.HTTPServiceUnavailable(req.method + " failed",
                                                description=error_msg,
                                                retry_after=30,
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
            group = Category.get(Category.id == int(id))
            group.delete_instance(recursive=True)

            res.status = falcon.HTTP_200
            res.body = json.dumps({"status": "Deletion successful"})

        except Exception as e:
            print(e)
            error_msg = ("Unable to delete group. Please try again later.")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_options(self, req, res, id):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

    def on_post(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_update(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)
