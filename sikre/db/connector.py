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

from peewee import *

from sikre import settings

try:
    db_conf = settings.DATABASE
    if db_conf['ENGINE'] == 'postgres':
        db = PostgresqlDatabase(
            db_conf['NAME'], user=db_conf['USER'],
            password=db_conf['PASSWORD'], host=db_conf['HOST'],
            port=db_conf['PORT'])
    else:
        db = SqliteDatabase(settings.DATABASE['NAME'])
except Exception as e:
    message = ("Couldn't connect to the database. Please check that your "
               "configuration is okay and the database exists.")
    logger.error(message)
    # This will leave the message in the WSGI logfile in case the other logger
    # fails
    print(message)


class ConnectionModel(Model):

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
