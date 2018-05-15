from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from sikr.db.connector import Base
from sikr.db.mixins import SikrModelMixin


user_group_table = Table('sikr_user_group_m2m', Base.metadata,
    Column('sikr_user', Integer, ForeignKey('sikr_user.id')),
    Column('sikr_usergroup', Integer, ForeignKey('sikr_usergroup.id'))
)


class UserGroup(Base, SikrModelMixin):

    """
    Basic model to group users.
    """
    name = Column(String)
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
    username = Column(String, unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    master_password = Column(String)

    def __repr__(self):
        """String representation of the object."""
        return f"<User: {self.username}>"
