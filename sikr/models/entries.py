import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sikr.db.connector import Base
from sikr.db.mixins import SikrModelMixin
from sikr.models.users import User


class Group(Base, SikrModelMixin):
    name = Column(String)
    #allowed_users = ManyToManyField(User, related_name='allowed_categories')

#UserCategory = Category.allowed_users.get_through_model()


class Entry(Base, SikrModelMixin):
    name = Column(String)
    description = Column(String)
    #allowed_users = ManyToManyField(User, related_name='allowed_items')
    pub_date = Column(DateTime(timezone=True), server_default=func.now())
    mod_date = Column(DateTime(timezone=True), onupdate=func.now())
    #tags = pw.CharField(null=True)
    #category = pw.ForeignKeyField(Category)

#UserItem = Item.allowed_users.get_through_model()
