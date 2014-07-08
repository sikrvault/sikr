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

# I don't like this, it's agains the PEP, but let's deal with it for now
from peewee import *

import settings

# Get the database or create it
db = SqliteDatabase(settings.DB_FILE)


class User(Model):
    #username
    #token
    #email
    #password
    pass


class Group(Model):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=255, unique=True)

    class Meta:
        database = db


class Item(Model):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField()
    description = TextField()
    group = ForeignKeyField(Group, related_name='group', null=True)

    class Meta:
        database = db


class Service(Model):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=255)
    username = CharField(max_length=255)
    password = CharField(max_length=255)
    url = CharField(max_length=255)
    tags = CharField()
    item = ForeignKeyField(Item, related_name='item')

    class Meta:
        database = db
