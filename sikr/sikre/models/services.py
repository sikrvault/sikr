import datetime

import peewee as orm

from sikre.db.connector import ConnectionModel
from sikre.models.items import Item
from sikre.models.users import User


class Service(ConnectionModel):
    name = orm.CharField(max_length=255)
    item = orm.ForeignKeyField(Item, backref='items')
    pub_date = orm.DateTimeField(default=datetime.datetime.now)
    allowed_users = orm.ManyToManyField(User, backref='allowed_services')

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
