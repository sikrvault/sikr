# Specify here the database settings for your MongoDB database. Currently we
# don't have support for no other engine.
DB_FILE = 'development.db'
DATABASE = {
    'NAME': '',       # Collection name
    'HOST': '',       # Server IP
    'PORT': 27017,    # Default: 27017
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

SITE_TITLE = 'Havas Worldwide London'
LOGO_IMAGE = '/static/images/havaslogo.jpg'
