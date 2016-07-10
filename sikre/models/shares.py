import binascii
import os

import peewee as orm

from sikre.db.connector import ConnectionModel
from sikre.models.users import User
from sikre.models.items import Category, Item
from sikre.models.services import Service


RESOURCE = (
    (0, "Category"),
    (1, "Item"),
    (2, "Service"),
)

USED = (
    (0, "No"),
    (1, "Yes"),
)


class ShareToken(ConnectionModel):

    """
    Standard user model. Stores minimal data about the user to handle the
    authentication, like email, username, and auth token, apart from some
    extra parameters for administration.
    """
    user = orm.ForeignKeyField(User)
    token = orm.CharField(unique=True, null=True)
    resource = orm.IntegerField(choices=RESOURCE, null=True)
    resource_id = orm.IntegerField(null=True)
    email = orm.CharField(null=True)
    used = orm.IntegerField(choices=USED, null=True)

    def is_valid(self):
        if self.used:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        return super(ShareToken, self).save(*args, **kwargs)
