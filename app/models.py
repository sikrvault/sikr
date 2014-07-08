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

# I don't like this, it's against the PEP, but let's deal with it for now
from peewee import *

import settings

# Get the database or create it
db = SqliteDatabase(settings.DB_FILE, threadlocals=True)


class ConnectionModel(Model):

    """
    This model acts as an abstract model that will create the database
    connection, which is necessary for all the models.
    """
    class Meta:
        database = db


class User(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    username = CharField(unique=True)
    name = CharField()
    token = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()


class Group(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=255, unique=True)


class Item(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField()
    description = TextField()
    group = ForeignKeyField(Group, related_name='group', null=True)
    author = ForeignKeyField(User, related_name='author')
    allowed_users = ForeignKeyField


class Service(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=255)
    username = CharField(max_length=255)
    password = CharField(max_length=255)
    url = CharField(max_length=255)
    tags = CharField()
    item = ForeignKeyField(Item, related_name='item')


# Try to create the database tables, don't do anything if they fail
try:
    User.create_table()
    Group.create_table()
    Item.create_table()
    Service.create_table()
except:
    pass
