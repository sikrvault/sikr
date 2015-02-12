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

from datetime import datetime, timedelta

import jwt

from sikre import settings


def create_jwt_token(user):
    payload = {
        'iss': 'localhost',
        'sub': user.id,
        'iat': datetime.now(),
        'exp': datetime.now() + timedelta(hours=settings.SESSION_EXPIRES)
    }
    token = jwt.encode(payload, settings.SECRET)
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, settings.SECRET)
