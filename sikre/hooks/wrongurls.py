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


def wrong_endpoint(req, resp, params):

    """Capture all the 404s on the API and send a response
    """
    if resp.status == '404':
        resp.status = falcon.HTTP_200
        resp.body = json.dumps([{"message": "This endpoint doesn't exist",
                                 "code": 404,
                                 "documentation": "http://docs.sikr.io"}])
