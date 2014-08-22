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

from sikre import settings


class TestResource(object):

    def on_get(self, request, response):
        try:
            result = {}
            result['version'] = settings.__version__
            result['codename'] = settings.__codename__
            result['status'] = settings.__status__
            response.status = falcon.HTTP_200
            response.body = json.dumps({"tests":[result]})
        except Exception as e:
            print(e)
            print(e.message)
            raise falcon.HTTPError(falcon.HTTP_500,
                                   "Server error",
                                   "Either there are no items or something went terribly wrong.")
