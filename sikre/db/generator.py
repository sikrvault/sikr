import sys

from faker import Faker

from sikre.models import users, items, services
from sikre.utils.logs import logger

fake = Faker()


def send_message(string):
    print(string, end='\r')
    sys.stdout.write("\033[K")


def generate_database(user=None):
    logger.info("Starting database generation")
    # Create a dummy user if there's no admin
    if not user:
        new_user = users.User.create(username="admin", email="example@example.com")
        new_user.set_master_password("admin")
        new_user.save()

    # Create 3 users
    user_counter = 3
    while user_counter > 0:
        user = users.User.create(username=fake.user_name(), email=fake.email())
        user.set_master_password("test")
        user.save()
        user_counter -= 1

        # Create some categories
        categories_counter = 3
        while categories_counter > 0:
            send_message(" * Creating groups, {0} remaining".format(categories_counter))
            new_category = items.Category.create(name=fake.user_name())
            new_category.save()
            new_category.allowed_users.add(user)
            categories_counter -= 1

            # Create some items
            items_counter = 5
            while items_counter > 0:
                send_message(" * Creating items for group {0}. {1} remaining".format(new_category.id, items_counter))
                new_item = items.Item.create(name=fake.name(), description=fake.text(), group=new_category)
                new_item.save()
                new_item.allowed_users.add(user)
                items_counter -= 1

                # Create some services
                services_counter = 4
                while services_counter > 0:
                    send_message(" * Creating services for item {0}. {1} remaining".format(new_item.id, services_counter))
                    new_service = services.Service.create(name=fake.company(),
                                                          username=fake.user_name(),
                                                          password=fake.password(),
                                                          url=fake.url(),
                                                          item=new_item)
                    new_service.save()
                    new_service.allowed_users.add(user)
                    services_counter -= 1
        logger.info("Database generation completed successfully")
