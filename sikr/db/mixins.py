from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Boolean


class SikrModelMixin(object):
    """Base model mixin for all Sikr models."""

    @declared_attr
    def __tablename__(cls):
        return f"sikr_{cls.__name__.lower()}"

    #__table_args__ = {'mysql_engine': 'InnoDB'}
    #__mapper_args__= {'always_refresh': True}

    id =  Column(Integer, primary_key=True)
    active = Column('Active', Boolean)
