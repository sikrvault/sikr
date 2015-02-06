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
from sikre.models.models import User, ItemGroup, Item, Service


class ItemsResource(object):

    def on_get(self, request, response):
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
            result = []
            services = []
            items_q = Item.select()
            services_q = Service.select()

            for i in services_q:
                services_dict = {}
                services_dict["id"] = i.pk
                services_dict["name"] = i.name
                services.append(services_dict)

            # Get all the items and put them into the list
            for i in items_q:
                item_dict = {}
                item_dict["name"] = i.name
                item_dict["description"] = i.description
                item_dict["services"] = services
                result.append(item_dict)

            response.status = falcon.HTTP_200
            response.body = json.dumps(result)
        except Exception as e:
            print(e)
            error_msg = ("A chicken got into the server farm! We will be back "
                         "as soon as we can get rid of it")
            raise falcon.HTTPServiceUnavailable(title="Service outage",
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_post(self, request, response):
        pass

    def on_put(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(request.method),
                               href=settings.__docs__)

    def on_update(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(request.method),
                               href=settings.__docs__)

    def on_delete(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(request.method),
                               href=settings.__docs__)
