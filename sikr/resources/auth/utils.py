from datetime import datetime, timedelta

import jwt

from sikre import settings


def create_jwt_token(user):
    payload = {
        'iss': settings.SITE_DOMAIN,
        'sub': user.id,
        'iat': datetime.now(),
        'exp': datetime.now() + timedelta(hours=settings.SESSION_EXPIRES)
    }
    token = jwt.encode(payload, settings.SECRET)
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.auth.split()[1]
    return jwt.decode(token, settings.SECRET)
