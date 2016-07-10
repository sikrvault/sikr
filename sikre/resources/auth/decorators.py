import datetime

import falcon

from sikre import settings
from sikre.resources.auth import utils
from sikre.utils.logs import logger


def login_required(req, res, resource, params):

    """Check the token to validate login state
    Check the JWT token sent by the frontend to see if the following conditions
    are NOT met:
        - Issuer host doesn't match the one specified in the settings file
        - Expiry timestamp is lower than the current timestamp
        - Issued timestamp is lower than the current timestamp minus SESSION_EXPIRES
    :returns: Redirect to the LOGIN_URL or HTTP 200
    """
    if req.auth:
        logger.debug("The user has a token in the header")
        payload = utils.parse_token(req)
        current_time = datetime.datetime.now()
        issue_time = current_time - datetime.timedelta(hours=settings.SESSION_EXPIRES)
        if payload['iss'] != settings.SITE_DOMAIN or \
           payload['exp'] <= int(current_time.timestamp()) or \
           payload['iat'] <= int(issue_time.timestamp()):

            logger.debug("JWT token expired or malformed")
            raise falcon.HTTPError(falcon.HTTP_401, title="Credentials expired",
                                   description="Your crendentials have expired. Please login again.")

        else:
            res.status = falcon.HTTP_200
    else:
        logger.debug("No JWT token found")
        raise falcon.HTTPError(falcon.HTTP_401, title="Credentials not found",
                               description="You don't have the credentials to access this resource")
