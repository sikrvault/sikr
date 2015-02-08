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


class GroupsResource(object):

    """Show all the groups that the current user has read permission.
    """
    def on_get(self, req, res):
        # Check user authentication
        try:
            result = []
            groups = ItemGroup.select()

            for group in groups:
                group_dict = {}
                group_dict["name"] = group.name
                result.append(group_dict)
        except Exception as e:
            print(e)
            error_msg = ("A chicken got into the server farm! We will be back "
                         "as soon as we can get rid of it")
            raise falcon.HTTPServiceUnavailable(title="Service outage",
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_post(self, request, response, pk):
        raise falcon.HTTPError(falcon.HTTP_405,
                               title="Client error",
                               description="{0} method not allowed.".format(request.method),
                               href=settings.__docs__)

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
