# Copyright 2014 Clione Software and Havas Worldwide London
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
from sikre.models.models import User, ItemGroup, Item, Service


class Items(object):

    def on_get(self, req, res):
        """
        Handle the GET request, returning a list of the items that the user
        has access to.

        First we create an empty dictionary and query the database to get
        all the item objects. After that, we iterate over the objects to
        populate the dictionary. In the end we return a 200 code to the browser
        and return the results dictionary wrapped in a list like the REsT
        standard says.
        """
        # Get the data
        try:
            payload = []
            items_q = Item.select()
            for item in items_q:
                # Clean the services
                services = []
                # Get all the services that belong to the item
                services_q = Service.select().where(Service.item == item)
                for service in services_q:
                    service_object = {}
                    service_object["id"] = service.pk
                    service_object["name"] = service.name
                    services.append(service_object)
                # Create the item object and append the services to it
                item_object = {}
                item_object["name"] = item.name
                item_object["description"] = item.description
                item_object["services"] = services
                payload.append(item_object)
            res.status = falcon.HTTP_200
            res.body = json.dumps(payload)
            logger.debug("Items request succesful")
        except Exception as e:
            logger.error(e)
            error_msg = ("Unable to get the items. Please try again later")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_post(self, req, res):
        pass

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


class DetailItem(object):

    """Show details of a specific group or add/delete a group
    """
    def on_get(self, req, res, pk):
        # Check user authentication
        try:
            group = ItemGroup.get(ItemGroup.pk == pk)

            payload = {}
            payload["name"] = group.name
            payload["id"] = group.pk

            res.status = falcon.HTTP_200
            res.body = json.dumps(payload)
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the group. Please try again later.")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_post(self, req, res, pk):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_put(self, req, res, pk):
        try:
            payload = json.loads(req.stream)
            group = ItemGroup.get(ItemGroup.pk == pk)
            pass

        except Exception as e:
            print(e)
            error_msg = ("Unable to update the group. Please try again later.")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_update(self, req, res, pk):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_delete(self, req, res, pk):
        try:
            group = ItemGroup.get(ItemGroup.pk == pk)
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
