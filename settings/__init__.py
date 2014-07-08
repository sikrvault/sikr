DEBUG = True
STAGING = False

if DEBUG and not STAGING:
    from . import development
elif STAGING:
    from . import staging
elif not DEBUG and not STAGING:
    from . import production

if DEBUG:
    import sys
    print(sys.path)
