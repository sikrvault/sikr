import falcon
import json

from sikre import settings


def get_platform_info():

    """Get basic information about the platform.
    """
    platform_info = {}
    platform_info['version'] = settings.__version__
    platform_info['codename'] = settings.__codename__
    platform_info['status'] = settings.__status__
    return platform_info


class TestResource(object):

    def on_get(self, request, response):
        try:
            result = {}
            result['platform_info'] = get_platform_info()
            response.status = falcon.HTTP_200
            response.body = json.dumps({"tests": result})
        except Exception as e:
            print(e)
            print(e.message)
            raise falcon.HTTPError(falcon.HTTP_500,
                                   "Server error",
                                   "Tests failed.")

    def on_options(self, req, res):

        """Acknowledge the OPTIONS method.
        """
        res.status = falcon.HTTP_200
