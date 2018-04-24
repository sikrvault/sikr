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
