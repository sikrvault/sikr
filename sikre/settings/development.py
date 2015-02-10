import os

# Add the current directory to the python path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Specify here the database settings. Currently we support only PostgreSQL and
# SQLite.
DATABASE = {
    'ENGINE': 'sqlite',        # 'postgres' for PostgreSQL or 'sqlite' for SQLite. Any other defaults to sqlite
    'NAME': 'development.db',  # Collection name. Filename for SQLite or DB name for PostgreSQL
    'HOST': '',                # Server IP. Default: localhost
    'PORT': '',                # Not needed for SQLite. PostgreSQL default: 5432
    'USER': '',                # Not needed for SQLite. User that has access to the DB
    'PASSWORD': '',            # Not needed for SQLite. Password for the user
}

# Restrict the extensions allowed for the uploaded files, we do other checks
# on the views, but this is the first level
ALLOWED_EXTENSIONS = [
    'cer', 'crt', 'pfx', 'key', 'pem', 'arm', 'crt',  # SSL files
]

# Select the default version of the API, this will load specific parts of your
# logic in the app.
DEFAULT_API = 'v1'

# Main server token, this is used as the second cycle cryptography. Make it
# unique and keep it away from strangers!
SECRET = '-&3whmt0f&h#zvyc@yk4bs3g6biu9l&a%0l=5u*q2+rz(sypdk'

# Logging settings. This is a standard python logging configuration.
LOGFILE = 'sikr.log'
LOG_CONFIG = {
    "version": 1,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(filename)s->%(funcName)s:%(lineno)s] %(message)s",
            'datefmt': "%Y/%m/%d %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, LOGFILE),
            'maxBytes': 2097152,  # 2MB per file
            'backupCount': 2,  # Store up to three files
            'formatter': 'standard',
        },
    },
    'loggers': {
        'sikr': {
            'handlers': ["logfile", ],
            'level': 'DEBUG',
        },
    }
}
