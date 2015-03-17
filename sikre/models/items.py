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
from playhouse.shortcuts import ManyToManyField

from sikre.db.connector import ConnectionModel
from sikre.models.users import User


class Category(ConnectionModel):
    name = pw.CharField(max_length=255, unique=True)
    allowed_users = ManyToManyField(User, related_name='allowed_categories')

UserCategory = Category.allowed_users.get_through_model()


class Item(ConnectionModel):
    name = pw.CharField()
    description = pw.TextField()
    allowed_users = ManyToManyField(User, related_name='allowed_items')
    pub_date = pw.DateTimeField(default=datetime.datetime.now)
    tags = pw.CharField(null=True)
    category = pw.ForeignKeyField(Category)

UserItem = Item.allowed_users.get_through_model()
