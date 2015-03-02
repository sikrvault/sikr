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

import peewee as orm
from playhouse.shortcuts import ManyToManyField

from sikre.db.connector import ConnectionModel
from sikre.models.items import Item
from sikre.models.users import User


class Service(ConnectionModel):
    name = orm.CharField(max_length=255)
    item = orm.ForeignKeyField(Item, related_name='items')
    pub_date = orm.DateTimeField(default=datetime.datetime.now)
    allowed_users = ManyToManyField(User, related_name='allowed_services')

    # Password
    username = orm.CharField(max_length=255, null=True)
    password = orm.CharField(max_length=255, null=True)
    url = orm.CharField(max_length=255, null=True)
    port = orm.IntegerField(null=True)
    extra = orm.TextField(null=True)

    # SSH
    ssh_title = orm.CharField(max_length=255, null=True)
    ssh_public = orm.TextField(null=True)
    ssh_private = orm.TextField(null=True)

    # SSL
    ssl_title = orm.CharField(max_length=255, null=True)
    ssl_filename = orm.CharField(max_length=255, null=True)

    # Other
    other = orm.TextField(null=True)

UserService = Service.allowed_users.get_through_model()
