import datetime

import peewee as orm
from playhouse.fields import ManyToManyField

from sikr.db.connector import ConnectionModel
from sikr.models.items import Item
from sikr.models.users import User


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
