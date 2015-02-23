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
import getpass
import hashlib
import uuid

from sikre.models import users
from sikre.utils.logs import logger
from sikre.utils.checks import check_python

check_python()


def create_superuser():

    """
    Create a superuser in the database that can manage everything
    """
    create_admin = input("\nDo you want to create an admin user? (Y/n) ")
    if create_admin in ['y', 'Y', 'yes', 'YES', None]:
        name = input("Full name: ")
        email = input("E-Mail address: ")
        username = input("Username (no spaces): ")
        password = getpass.getpass("Password (we don't ask twice!): ")

        # Process the password for storage
        salt = uuid.uuid4().hex.encode('utf-8')
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt).hexdigest()

        # Create the user object in the database
        new_user = users.User.create(name=name, email=email, username=username,
                                     password=hashed_password, is_superuser=True)
        new_user.save()
        return new_user
    else:
        logger.info("Admin user not created. You can create it afterwards.\n")
