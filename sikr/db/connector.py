"""Main database connector module.

This module organizes the connections to teh database accrding to the settings
file and values provided. It also creates a base model from where the rest of
models have to inherit from so they connect to the same database.
"""
import sys
import logging

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sikr import settings

logger = logging.getLogger(__name__)


def get_dict_values(dict, key, default_value=''):
    """Get the dictionary values accounting for empty values when key exists."""
    # Returns False if key doesnt exist, False if value is empty
    if bool(dict.get(key)):
        return dict.get(key)
    else:
        return default_value


db_conf = settings.DATABASE
db_user = get_dict_values(db_conf, 'USER', 'root')
db_host = get_dict_values(db_conf, 'HOST', 'localhost')
db_name = get_dict_values(db_conf, 'NAME', 'mydatabase')
db_engine = get_dict_values(db_conf, 'ENGINE')
db_password = get_dict_values(db_conf, 'PASSWORD')
db_postgres_port = get_dict_values(db_conf, 'PORT', '5432')
db_mysql_port = get_dict_values(db_conf, 'PORT', '3306')

if db_engine == 'postgresql':
    engine = sqlalchemy.create_engine("{}://{}:{}@{}:{}/{}".format(
        db_engine, db_user, db_password, db_host, db_postgres_port, db_name
    ))
elif db_engine == 'mysql':
    engine = sqlalchemy.create_engine("{}://{}:{}@{}:{}/{}".format(
        db_engine, db_user, db_password, db_host, db_mysql_port, db_name
    ))
elif db_engine == 'sqlite':
    engine = sqlalchemy.create_engine("{}:///{}".format(db_engine, db_name))
else:
    error_msg = "Database engine not supported. Valid options are: postgresql, mysql, sqlite"
    logger.error(error_msg)
    sys.exit(error_msg)

# Establish declarative mapping for models
Base = declarative_base()

# Establish ORM DB session
Session = sessionmaker(bind=engine)
