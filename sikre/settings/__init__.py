DEBUG = True
STAGING = False

if DEBUG and not STAGING:
    from .development import *
elif STAGING:
    from .staging import *
elif not DEBUG and not STAGING:
    from .production import *
