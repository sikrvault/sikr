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
from sikre.models.services import Service
from sikre.resources.auth.decorators import login_required


@falcon.before(login_required)
class DetailService(object):

    """
    This resource handles the /services/ url.
    """
    def on_get(self, req, res, id):
        # Get the data
        try:
            payload = []
            service = Service.get(Service.id == id)

            # Get all the services and organize them
            services_dict = {}
            services_dict["url"] = service.url
            services_dict["username"] = service.username
            services_dict["password"] = service.password
            payload.append(services_dict)

            res.status = falcon.HTTP_200
            res.body = json.dumps(payload)
        except Exception as e:
            print(e)
            error_msg = ("Unable to get the items. Please try again later")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_post(self, req, res, id):
        pass

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200

    def on_put(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_update(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_delete(self, req, res, id):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)


@falcon.before(login_required)
class Services(object):

    def on_get(self, req, res):
        """
        Handle the GET request, returning a list of the items that the user
        has access to.

        First we create an empty dictionary and query the database to get
        all the item objects. After that, we iterate over the objects to
        populate the dictionary. In the end we return a 200 code to the browser
        and return the results dictionary wrapped in a list like the ReST
        standard says.
        """
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(req.method),
                               href=settings.__docs__)

    def on_post(self, request, response, pk):
        pass

    def on_put(self, request, response, pk):
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
