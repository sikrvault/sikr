from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from sikr.db.connector import Base
from sikr.db.mixins import SikrModelMixin


user_group_table = Table('sikr_user_group_m2m', Base.metadata,
    Column('sikr_user', Integer, ForeignKey('user.id')),
    Column('sikr_group', Integer, ForeignKey('group.id'))
)


class Group(Base, SikrModelMixin):

    """
    Basic model to group users.
    """
    name = Column('Name', String)
    users = relationship("User",
                         secondary=user_group_table,
                         backref="groups")

    def __repr__(self):
        """String representation of the object."""
        return f"<Group: {self.name}"


class User(Base, SikrModelMixin):
    """Standard user model.

    Stores minimal data about the user to handle the
    authentication, like email, username, and auth token, apart from some
    extra parameters for administration.
    """
    username = Column('Username', String, unique=True)
    name = Column('Name', String)
    email = Column('E-Mail', String, unique=True)
    master_password = Column('Master Password', String)

    def __repr__(self):
        """String representation of the object."""
        return f"<User: {self.username}>"
