# Specify here the file that will store you SQLite database. We don't give a
# choice in databases to prevent external access to it.
DB_FILE = 'development.db'

# Restrict the extensions allowed for the uploaded files, we do other checks
# on the views, but this is the first level
ALLOWED_EXTENSIONS = ['cer', 'pfx', 'key', 'pem', 'arm', 'crt']

# Select the default version of the API, this will load specific parts of your
# logic in the app.
DEFAULT_API = 'v1'