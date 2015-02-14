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

import datetime

import peewee as pw

from sikre.db.connector import ConnectionModel
from sikre.models.items import Item


class Service(ConnectionModel):
    name = pw.CharField(max_length=255)
    username = pw.CharField(max_length=255)
    password = pw.CharField(max_length=255)
    url = pw.CharField(max_length=255)

    # file =
    item = pw.ForeignKeyField(Item, related_name='items')
    pub_date = pw.DateTimeField(default=datetime.datetime.now)
