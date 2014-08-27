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

import datetime
# I don't like this, it's against the PEP, but let's deal with it for now
from peewee import *

from sikre import settings

# Get the database or create it
db = SqliteDatabase(settings.DB_FILE, threadlocals=True)


class ConnectionModel(Model):

    """
    This model acts as an abstract model that will create the database
    connection, which is necessary for all the models.
    """
    def __str__(self):
        """
        Return JSON ready data if any model is accesed through the str method
        """
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return str(r)

    class Meta:
        """
        Connect all the models to the same database.
        """
        database = db


class User(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    username = CharField(unique=True)
    name = CharField()
    token = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    date_joined = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)


class Group(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=255, unique=True)


class Item(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField()
    description = TextField()
    group = ForeignKeyField(Group, related_name='group', null=True)
    author = ForeignKeyField(User, related_name='author')
    pub_date = DateTimeField(default=datetime.datetime.now)
    allowed_users = ForeignKeyField(User, related_name='allowed_users')
    tags = CharField(null=True)


class Service(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=255)
    username = CharField(max_length=255)
    password = CharField(max_length=255)
    url = CharField(max_length=255)
    #file =
    item = ForeignKeyField(Item, related_name='item')
    pub_date = DateTimeField(default=datetime.datetime.now)


# Try to create the database tables, don't do anything if they fail
try:
    User.create_table()
    Group.create_table()
    Item.create_table()
    Service.create_table()
except:
    pass
