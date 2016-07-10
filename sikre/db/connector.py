"""Main database connector module.

This module organizes the connections to teh database accrding to the settings
file and values provided. It also creates a base model from where the rest of
models have to inherit from so they connect to the same database.
"""

import json

import peewee as orm

from sikre import settings
from sikre.utils.logs import logger

try:
    db_conf = settings.DATABASE
    # Set the defaults in case something happens
    db_user = settings.DATABASE.get("USER", 'root')
    db_host = settings.DATABASE.get("HOST", 'localhost')
    db_postgres_port = settings.DATABASE.get("PORT", '5432')
    db_mysql_port = settings.DATABASE.get("PORT", '3306')

    if db_conf['ENGINE'] == 'postgres':
        db = orm.PostgresqlDatabase(db_conf['NAME'], user=db_user,
                                    password=db_conf['PASSWORD'],
                                    host=db_host, port=db_postgres_port)
        logger.debug("Connected to the PostgreSQL database")

    elif db_conf['ENGINE'] == 'mysql':
        db = orm.MySQLDatabase(db_conf['NAME'], user=db_user,
                               password=db_conf['PASSWORD'],
                               host=db_host, port=db_mysql_port)
        logger.debug("Connected to the MySQL database")

    else:
        db = orm.SqliteDatabase(settings.DATABASE['NAME'])
        logger.debug("Connected to the SQLite database")
except Exception as e:
    message = ("Couldn't connect to the database. Please check that your "
               "configuration is okay and the database exists.")
    logger.critical(message)
    # This will leave the message in the WSGI logfile in case the other logger
    # fails
    print(message)


class ConnectionModel(orm.Model):
    """Connection abstract model.

    This model will abstract some of the functionality required across all
    the data models in the application.

    Returns:
        database: the database connection for the model
        __str__: the data returned as a JSON string
    """

    def __str__(self):
        """Return JSON data if any model is accesed through the str method."""
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return str(r)

    class Meta:
        """Connect all the models to the same database."""

        database = db
