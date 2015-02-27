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
from sikre.models.items import ItemGroup, Item
from sikre.models.services import Service
from sikre.resources.auth.decorators import login_required
from sikre.resources.auth.utils import parse_token


class Items(object):

    @falcon.before(login_required)
    def on_get(self, req, res):
        """Get the items that belong to that user.

        This method contains two behaviours, one returns
        Handle the GET request, returning a list of the items that the user
        has access to.

        First we create an empty dictionary and query the database to get
        all the item objects. After that, we iterate over the objects to
        populate the dictionary. In the end we return a 200 code to the browser
        and return the results dictionary wrapped in a list like the REsT
        standard says.
        """
        payload = {}
        # Parse token and get user id
        user_id = parse_token(req)['sub']

        try:
            # Get the user
            user = User.get(User.id == int(user_id))
            # See if we have to filter by group
            filter_group = req.get_param("group", required=False)
            if filter_group:
                # Get the group
                group = (ItemGroup.select(ItemGroup.name, ItemGroup.id)
                                  .where(ItemGroup.id == int(filter_group))
                                  .get())
                payload["group_name"] = str(group.name)
                payload["group_id"] = int(group.id)
                items = list(user.allowed_items
                                 .select(Item.name, Item.description, Item.id)
                                 .where(Item.group == int(filter_group))
                                 .dicts())
                logger.debug("Got items filtered by group and user")
            else:
                payload["group"] = "All"
                items = list(user.allowed_items
                             .select(Item.name, Item.description, Item.id)
                             .dicts())
                logger.debug("Got all items")
            for item in items:
                services = list(user.allowed_services
                                    .select(Service.id, Service.name)
                                    .where(Service.item == item["id"])
                                    .dicts())
                item["services"] = services
            payload["items"] = items
            res.status = falcon.HTTP_200
            res.body = json.dumps(payload)
            logger.debug("Items request succesful")
        except Exception as e:
            print(e)
            logger.error(e)
            error_msg = ("Unable to get the items. Please try again later")
            raise falcon.HTTPServiceUnavailable(title=req.method + " failed",
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    @falcon.before(login_required)
    def on_post(self, req, res):

        """Save a new item
        """
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
            new_item = Item.create(name=result_json.get('name'),
                                   description=result_json.get("description", ''),
                                   group=result_json.get("group"),
                                   tags=result_json.get("tags", ''))
            new_item.save()
            new_item.allowed_users.add(user)
        except Exception as e:
            raise falcon.HTTPInternalServerError(title="Error while saving the item",
                                                 description=e,
                                                 href=settings.__docs__)

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

    def on_put(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)

    def on_update(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)

    def on_delete(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)


class DetailItem(object):

    """Show details of a specific group or add/delete a group
    """
    @falcon.before(login_required)
    def on_get(self, req, res, id):
        user_id = parse_token(req)['sub']
        try:
            user = User.get(User.id == int(user_id))
            item = Item.get(Item.id == int(id))
            if user not in item.allowed_users:
                raise falcon.HTTPForbidden(title="Permission denied",
                                           description="You don't have access to this resource",
                                           href=settings.__docs__)
            res.status = falcon.HTTP_200
            res.body = json.dumps(item)
            logger.debug("Items request succesful")
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the item. Please try again later.")
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
            item = Item.get(Item.id == int(id))
            if user not in item.allowed_users:
                raise falcon.HTTPForbidden(title="Permission denied",
                                           description="You don't have access to this resource",
                                           href=settings.__docs__)
            item.name = result_json.get("name", item.name)
            item.description = result_json.get("description", item.description)
            item.group = result_json.get("group", item.group)
            item.tags = result_json.get("tags", item.tags)
            item.save()
            res.status = falcon.HTTP_200
            res.body = json.dumps({"message": "Item updated"})
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the item. Please try again later.")
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
            item = Item.get(Item.id == int(id))
            if user not in item.allowed_users:
                raise falcon.HTTPForbidden(title="Permission denied",
                                           description="You don't have access to this resource",
                                           href=settings.__docs__)
            item.delete_instance()
            res.status = falcon.HTTP_200
            res.body = json.dumps({"message": "Deletion successful"})

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
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)

    def on_update(self, req, res):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description=req.method + " method not allowed.",
                               href=settings.__docs__)
