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
from sikre.models.users import User
from sikre.models.items import ItemGroup
from sikre.resources.auth.decorators import login_required
from sikre.resources.auth.utils import parse_token


class Groups(object):

    """Show all the groups that the current user has read permission.

    This resource will send the ItemGroups that belong to the user in the
    matter of ID and NAME
    """
    @falcon.before(login_required)
    def on_get(self, req, res):
        # Parse token and get user id
        user_id = parse_token(req)['sub']

        # Check user authentication
        try:
            # Get the user
            user = User.get(User.id == int(user_id))

            groups = list(user.allowed_itemgroups
                              .select(ItemGroup.id, ItemGroup.name)
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
        pass

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


@falcon.before(login_required)
class DetailGroup(object):

    """Show details of a specific group or add/delete a group
    """
    @falcon.before(login_required)
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
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    @falcon.before(login_required)
    def on_post(self, req, res, id):
        try:
            payload = json.loads(req.stream)
            group = ItemGroup.get(ItemGroup.id == id)
            pass

        except Exception as e:
            print(e)
            error_msg = ("Unable to update the group. Please try again later.")
            raise falcon.HTTPServiceUnavailable(title="{0} failed".format(req.method),
                                                description=error_msg,
                                                retry_after=30,
                                                href=settings.__docs__)

    def on_options(self, req, res, id):

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
