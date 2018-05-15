from sikr.db.connector import Base, engine
from sikr.models.users import UserGroup, User
from sikr.models.entries import Group, Entry
from sikr.utils.logs import logger


def generate_schema():
    """Generate the initial schema for the database."""
    start_msg = "Creating database schema..."
    end_msg = "Database schema created"
    print(f"[ --  ] {start_msg}")
    logger.info(start_msg)
    try:
        Base.metadata.create_all(engine)
        print(f"[ OK  ] {end_msg}")
        logger.info(end_msg)
    except Exception as e:
        error_msg = f"Error creating schema: {e}"
        print(f"[ERROR] {error_msg}")
        logger.error(error_msg)
        sys.exit(1)
