import datetime

import peewee as pw

from sikre.db.connector import ConnectionModel
from sikre.models.users import User


class Category(ConnectionModel):
    name = pw.CharField(max_length=255, unique=True)
    allowed_users = pw.ManyToManyField(User, backref='allowed_categories')

UserCategory = Category.allowed_users.get_through_model()


class Item(ConnectionModel):
    name = pw.CharField()
    description = pw.TextField()
    allowed_users = pw.ManyToManyField(User, backref='allowed_items')
    pub_date = pw.DateTimeField(default=datetime.datetime.now)
    tags = pw.CharField(null=True)
    category = pw.ForeignKeyField(Category)

UserItem = Item.allowed_users.get_through_model()
