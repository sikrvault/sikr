"""Main development settings."""

import os

# Add the current directory to the python path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Specify here the database settings. We support MySQL, PostgreSQL and SQLite
DATABASE = {
    'ENGINE': 'sqlite',        # 'postgres', 'sqlite' or 'mysql'. Any other defaults to sqlite
    'NAME': 'development.db',  # Filename for SQLite or DB name for PostgreSQL/MySQL
    'HOST': '',                # Not needed for SQLite. Server IP. Default: localhost
    'PORT': '',                # Not needed for SQLite. PostgreSQL default: 5432
    'USER': '',                # Not needed for SQLite. User that has access to the DB
    'PASSWORD': '',            # Not needed for SQLite. Password for the user
}

# Restrict the extensions allowed for the uploaded files, we do other checks
# on the views, but this is the first level
ALLOWED_EXTENSIONS = [
    'cer', 'crt', 'pfx', 'key', 'pem', 'arm', 'crt', 'pub'
]

# Select the default version of the API, this will load specific parts of your
# logic in the app.
DEFAULT_API = 'v1'

# Site domain, you usually want this to be your frontend url. This is used for
# login verification between other things like CORS
CORS_ACTIVE = True
SITE_DOMAIN = 'https://sikr.io'
LOGIN_URL = 'http://sikr.io/login.html'

# This rewrites the response "Server" header, so you can hide your server name
# for protection
SERVER_NAME = "sikr.io"

# How long the user session will last (in hours). Default: 168 (7 days)
SESSION_EXPIRES = 168

# Service tokens, this are usually the "client secret" or private API keys
# that you need to finish the OAuth validation. Remember NOT to commit back
# this values! They should remain known to you only!
GITHUB_SECRET = ''
FACEBOOK_SECRET = ''
LINKEDIN_SECRET = ''
GOOGLEPLUS_SECRET = ''
TWITTER_KEY = ''
TWITTER_SECRET = ''  # Twitter consumer secret
TWITTER_CALLBACK_URI = ''

# Main server token Make it unique and keep it away from strangers! This token
# is used in authentication and part of the storage encryption. This token
# is an example. **You MUST replace it!**
SECRET = '-&3whmt0f&h#zvyc@yk4bs3g6biu9l&a%0l=5u*q2+rz(sypdk'

# Email SMTP settings.
DEFAULT_EMAIL_FROM = 'noreply@sikr.io'
SMTP_SERVER = ''
SMTP_PORT = 587
SMTP_USER = ''
SMTP_PASSWORD = ''
SMTP_TLS = True

# Logging settings. This is a standard python logging configuration. The levels
# are supposed to change depending on the settings file, to avoid clogging the
# logs with useless information.
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
            'maxBytes': 10485760,  # 10MB per file
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
