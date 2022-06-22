import requests
from ..exceptions import InvalidParams
import logging

logger = logging.getLogger("__name__")


def baato_places(*args, **kwargs):
    baato_url = kwargs.pop("baseURL")
    access_key = kwargs.pop("access_token")
    if "place_id" not in kwargs:
        raise InvalidParams("place_id parameter must be provide for search request")

    try:
        placeId = kwargs.pop("place_id")
        res = requests.get(f"{baato_url}places?key={access_key}&placeId={placeId}")
        return res
    except requests.exceptions.RequestException as err:
        logger.debug(f"Exception occure in places API {err}")
