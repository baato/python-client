import logging
from baato import exceptions
from baato.resources import baato_search
from baato.resources import baato_reverse_search
from baato.resources import baato_places
from baato.resources import baato_near_by
from baato.resources import baato_direction
from baato.resources import baato_map_style
from baato.resources import url_validator
from baato.config import __baato_endpoint__, __baato_version__

logger = logging.getLogger(__name__)


class BaatoApi(object):
    def __init__(self, access_token=None, endpoint=None, version=None, *args, **kwargs):
        """
        Create API object
        """
        self.endpoint = self.validate_endpoint(endpoint) if endpoint else __baato_endpoint__
        self.version = self.validate_version(version) if version else __baato_version__
        self.access_token = self.validate_access_token(access_token)

        self.baseURL = self.get_baseURL(self.endpoint, self.version)

    @staticmethod
    def validate_access_token(access_token):
        if not access_token:
            raise exceptions.InvalidConfig("access_token must provide")
        return access_token

    @staticmethod
    def validate_endpoint(endpoint):
        if endpoint and url_validator(endpoint):
            return endpoint.rstrip("/")
        else:
            raise exceptions.InvalidConfig("Endpoint is Invalid", "Received: %s" % (endpoint))

    @staticmethod
    def validate_version(version):
        if version and version in [
            "v1",
        ]:
            return version
        raise exceptions.InvalidConfig("Version is Invalid", "Received: %s" % (version))

    @staticmethod
    def get_baseURL(endpoint, version):
        """Create the absolute baato API url

        Args:
            endpoint (str):
            version (str):

        Returns:
            str:
        """
        return "%s/%s/" % (endpoint, version)

    def search(self, *args, **params):
        """Baato search API # https://docs.baato.io/#/v1/services/search
        Returns:
            json:
        """
        response = baato_search(access_token=self.access_token, baseURL=self.baseURL, **params)
        return response.json()

    def reverse(self, *args, **params):
        """Baato Reverse API # https://docs.baato.io/#/v1/services/reverse

        Returns:
            json:
        """
        response = baato_reverse_search(access_token=self.access_token, baseURL=self.baseURL, **params)
        return response.json()

    def places(self, *args, **params):
        """Baato Places API # https://docs.baato.io/#/v1/services/places

        Returns:
            json:
        """
        response = baato_places(access_token=self.access_token, baseURL=self.baseURL, **params)
        return response.json()

    def near_by(self, *args, **params):
        """Baato NearBy API # https://docs.baato.io/#/v1/services/nearby_places

        Returns:
            json:
        """
        response = baato_near_by(access_token=self.access_token, baseURL=self.baseURL, **params)
        return response.json()

    def direction(self, *args, **params):
        """Baato Direction API # https://docs.baato.io/#/v1/services/directions

        Returns:
            json:
        """
        response = baato_direction(access_token=self.access_token, baseURL=self.baseURL, **params)
        return response.json()

    def map_style(self, *args, **params):
        """Baato Map style API # https://docs.baato.io/#/v1/services/styles

        Returns:
            json:
        """
        response = baato_map_style(access_token=self.access_token, baseURL=self.baseURL, **params)
        return response.json()


class BaatoClient(BaatoApi):
    pass
