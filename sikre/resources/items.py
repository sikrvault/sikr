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
        try:
            payload = []
            filter_group = req.get_param("group", required=False)
            if filter_group:
                items = (Item.select(Item.name, Item.description, Item.id)
                             .where(Item.group == int(filter_group))
                             .dicts())
                logger.debug("Got items filtered by group")
            else:
                items = (Item.select(Item.name, Item.description, Item.id)
                             .dicts())
                logger.debug("Got all items")
            for item in items:
                services = list(Service.select(Service.id, Service.name)
                                       .where(Service.item == item["id"])
                                       .dicts())
                item["services"] = services
                payload.append(item)
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

    def on_post(self, req, res):
        pass

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
    def on_get(self, req, res, id):
        # Check user authentication
        try:
            group = ItemGroup.get(ItemGroup.id == id)

            payload = {}
            payload["name"] = group.name
            payload["id"] = group.pk

            res.status = falcon.HTTP_200
            res.body = json.dumps(payload)
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the group. Please try again later.")
            raise falcon.HTTPServiceUnavailable(req.method + " failed",
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_post(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_put(self, req, res, id):
        try:
            payload = json.loads(req.stream)
            group = ItemGroup.get(ItemGroup.pk == id)
            pass

        except Exception as e:
            print(e)
            error_msg = ("Unable to update the group. Please try again later.")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_update(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_delete(self, req, res, id):
        try:
            group = ItemGroup.get(ItemGroup.pk == id)
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
