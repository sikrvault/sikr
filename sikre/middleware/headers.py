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


class BaseHeaders(object):
    def process_request(self, req, res):

        """Force some required headers inside every request and response

        We intercept all the requests and responses and add some required
        headers for the API interaction.
        """
        res.set_headers({
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, x-auth-user, x-auth-password, Authorization',
            'Access-Control-Allow-Methods': 'GET, PUT, POST, OPTIONS, DELETE'
        })

    def process_response(self, req, res, resource):

        res.set_headers({
            'Cache-Control': 'no-store, must-revalidate, no-cache, max-age=0',
            'Content-Type': 'application/json',
            'Server': 'sikr.io',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, x-auth-user, x-auth-password, Authorization',
            'Access-Control-Allow-Methods': 'GET, PUT, POST, OPTIONS, DELETE'
        })
