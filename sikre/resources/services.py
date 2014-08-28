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

import falcon
import json

from sikre.models.models import User, ItemGroup, Item, Service


class AddServicesResource(object):

    """
    This resource handles the /services/ url.
    """
    def on_get(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The GET method is not allowed in this endpoint.")

    def on_post(self, request, response):
        pass

    def on_put(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The PUT method is not allowed in this endpoint.")

    def on_update(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The UPDATE method is not allowed in this endpoint.")

    def on_delete(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The DELETE method is not allowed in this endpoint.")


class ServicesResource(object):

    def on_get(self, request, response, pk):
        """
        Handle the GET request, returning a list of the items that the user
        has access to.

        First we create an empty dictionary and query the database to get
        all the item objects. After that, we iterate over the objects to
        populate the dictionary. In the end we return a 200 code to the browser
        and return the results dictionary wrapped in a list like the ReST
        standard says.
        """
        # Get the data
        try:
            result = []
            service = Service.get(pk=pk)

            # Get all the services and organize them
            services_dict = {}
            services_dict["url"] = service.url
            services_dict["username"] = service.username
            services_dict["password"] = service.password
            result.append(services_dict)

            response.status = falcon.HTTP_200
            response.body = json.dumps({"services":result})
        except Exception as e:
            print(e)
            raise falcon.HTTPError(falcon.HTTP_500,
                                   "Server error",
                                   "Either there are no items or something went terribly wrong.")

    def on_post(self, request, response):
        raise falcon.HTTPError(falcon.HTTP_405, "Client error",
                               "The POST method is not allowed in this endpoint.")

    def on_put(self, request, response):
        pass

    def on_update(self, request, response):
        pass

    def on_delete(self, request, response):
        pass
