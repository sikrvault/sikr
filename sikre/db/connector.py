# Copyright 2014-2015 Clione Software and Havas Worldwide London
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Set the database. This creates a connection to the PostgreSQL or SQLite
# databases according to the settings.
# TODO: Move the connector out of the models

import json

import peewee as orm

from sikre import settings
from sikre.utils.logs import logger

try:
    db_conf = settings.DATABASE
    # Set the defaults in case something happens
    db_user = settings.DATABASE["USER"] or 'root'
    db_host = settings.DATABASE["HOST"] or 'localhost'
    db_postgres_port = settings.DATABASE["PORT"] or '5432'
    db_mysql_port = settings.DATABASE["PORT"] or '3306'

    if db_conf['ENGINE'] == 'postgres':
        db = orm.PostgresqlDatabase(
            db_conf['NAME'], user=db_user, password=db_conf['PASSWORD'],
            host=db_host, port=db_postgres_port)
        logger.debug("Connected to the PostgreSQL database")
    elif db_conf['ENGINE'] == 'mysql':
        db = orm.MySQLDatabase(
            db_conf['NAME'], user=db_user, password=db_conf['PASSWORD'],
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

    """This model will abstract some of the functionality required across all
    the data models in the application.

    Returns:
        database: the database connection for the model
        __str__: the data returned as a JSON string
    """
    def __str__(self):
        """
        Return JSON ready data if any model is accesed through the str method
        """
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        return str(r)

    class Meta:
        """
        Connect all the models to the same database.
        """
        database = db
