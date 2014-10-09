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
import crypt
import hmac

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


######################
# User block
######################

class User(ConnectionModel):

    """
    Standard user model. Stores minimal data about the user to handle the
    authentication, like email, username, and auth token, apart from some
    extra parameters for administration.
    """
    pk = PrimaryKeyField(primary_key=True)
    username = CharField(unique=True)
    token = CharField(unique=True)
    password = CharField(unique=True)
    email = CharField(unique=True)

    # Social JWT storage
    facebook = CharField(unique=True)
    google = CharField(unique=True)
    github = CharField(unique=True)
    linkedin = CharField(unique=True)
    twitter = CharField(unique=True)

    # Data
    join_date = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)

    def set_password(self, password):
        """
        Method to set the password of the user. If the user registers through
        social networks, this method will be called to create a scrambled
        password.
        """
        hashed_password = crypt.crypt(password)
        self.password = hashed_password

    def check_password(self, password):
        """
        Method to check that the sent password matches the password in
        """
        check = hmac.compare_digest(crypt.crypt(password, self.password), self.password)
        if not check:
           raise ValueError("hashed version doesn't validate against original")
        else:
            return True


class UserGroup(ConnectionModel):

    """
    Basic model to group users.
    """
    pk = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=255, unique=True)
    pub_date = DateTimeField(default=datetime.datetime.now)


class GroupToUser(ConnectionModel):

    """
    Trough table for the many to many between group and user.
    """
    user = ForeignKeyField(User)
    group = ForeignKeyField(UserGroup)

    class Meta:
        primary_key = CompositeKey('group', 'user')


######################
# Item block
######################

class ItemGroup(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=255, unique=True)


class Item(ConnectionModel):
    pk = PrimaryKeyField(primary_key=True)
    name = CharField()
    description = TextField()
    author = ForeignKeyField(User, related_name='author')
    pub_date = DateTimeField(default=datetime.datetime.now)
    tags = CharField(null=True)


class ItemGroupToItem(ConnectionModel):

    """
    Trough table for the many to many between item groups and items.
    """
    item = ForeignKeyField(Item)
    itemgroup = ForeignKeyField(ItemGroup)

    class Meta:
        primary_key = CompositeKey('itemgroup', 'item')


class UserToItem(ConnectionModel):

    """
    Trough table for the many to many between users and items, this table
    determines which user can access what item.
    """
    item = ForeignKeyField(Item)
    user = ForeignKeyField(User)

    class Meta:
        primary_key = CompositeKey('user', 'item')


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
    UserGroup.create_table()
    GroupToUser.create_table()

    ItemGroup.create_table()
    Item.create_table()
    ItemGroupToItem.create_table()
    UserToItem.create_table()
    Service.create_table()
except:
    pass
