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


from sikre.db.connector import db
from sikre.models import users, items, services, shares
from sikre.utils.logs import logger
from sikre.utils.checks import check_python

check_python()


def generate_db_schema():
    # Try to create the database tables, don't do anything if they fail
    try:
        print(" * Syncing database tables...")
        # First set the m2m models
        logger.info("Attempting to create the tables")
        db.create_tables([
            users.User,
            users.Group,
            users.UserGroup,
            items.Category,
            items.UserCategory,
            items.UserItem,
            items.Item,
            services.Service,
            services.UserService,
            shares.ShareToken,
        ])
        print(" * Database tables created")
    except Exception as e:
        logger.error(e)
        print(e)
