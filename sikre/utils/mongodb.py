# Copyright 2014 Clione Software and Havas Worldwide London
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

import sys

from sikre.settings import DATABASE

from pymongo import MongoClient


def connect_to_database():

    """
    Try to connect to the database and the collection, if something happens
    we break the application, since it cannot run without a database.
    """
    try:
        connection = MongoClient(DATABASE['HOST'], DATABASE['PORT'])
        db = connection[DATABASE['NAME']]
    except Exception as e:
        print("ERROR: Something went wrong while connecting to the database.")
        sys.exit(e)


def read_from_collection()
